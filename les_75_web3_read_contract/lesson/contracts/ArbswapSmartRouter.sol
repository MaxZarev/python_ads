// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/access/Ownable.sol";

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

import "./interfaces/IStableSwap.sol";
import "./interfaces/IStableSwapFactory.sol";
import "./interfaces/IArbswapV2Factory.sol";
import "./interfaces/IWETH02.sol";
import "./libraries/UniERC20.sol";
import "./libraries/SafeERC20.sol";
import "./libraries/ArbswapV2ExchangeLib.sol";

contract ArbswapSmartRouter is Ownable, ReentrancyGuard {
    using UniERC20 for IERC20;
    using SafeERC20 for IERC20;
    using ArbswapV2ExchangeLib for IArbswapV2Exchange;

    enum FLAG {
        STABLE_SWAP, // 0
        V2_EXACT_IN // 1
    }

    IWETH02 public immutable weth;
    address public immutable arbswapV2;
    address public stableswapFactory;

    event NewStableSwapFactory(address indexed sender, address indexed factory);
    event SwapMulti(
        address indexed sender,
        address indexed srcTokenAddr,
        address indexed dstTokenAddr,
        uint256 srcAmount
    );
    event Swap(
        address indexed sender,
        address indexed srcTokenAddr,
        address indexed dstTokenAddr,
        uint256 srcAmount
    );

    fallback() external {}

    receive() external payable {}
    /*
     * @notice Constructor
     * @param _WETHAddress: address of the WETH contract
     * @param _arbswapV2: address of the ArbswapFactory
     * @param _stableswapFactory: address of the StableSwapFactory
     */
    constructor(
        address _WETHAddress,
        address _arbswapV2,
        address _stableswapFactory
    ) {
        weth = IWETH02(_WETHAddress);
        arbswapV2 = _arbswapV2;
        stableswapFactory = _stableswapFactory;
    }

    /**
     * @notice Sets treasury address
     * @dev Only callable by the contract owner.
     */
    function setStableSwapFactory(address _factory) external onlyOwner {
        require(
            _factory != address(0),
            "StableSwap factory cannot be zero address"
        );
        stableswapFactory = _factory;
        emit NewStableSwapFactory(msg.sender, stableswapFactory);
    }

    function swapMulti(
        IERC20[] calldata tokens,
        uint256 amount,
        uint256 minReturn,
        FLAG[] calldata flags
    ) public payable nonReentrant returns (uint256 returnAmount) {
        require(tokens.length == flags.length + 1, "swapMulti: wrong length");

        IERC20 srcToken = tokens[0];
        IERC20 dstToken = tokens[tokens.length - 1];

        if (srcToken == dstToken) {
            return amount;
        }

        srcToken.uniTransferFrom(payable(msg.sender), address(this), amount);

        uint256 receivedAmount = srcToken.uniBalanceOf(address(this));

        for (uint256 i = 0; i < tokens.length; i++) {
            if (tokens[i - 1] == tokens[i]) {
                continue;
            }

            if (flags[i - 1] == FLAG.STABLE_SWAP) {
                _swapOnStableSwap(
                    tokens[i - 1],
                    tokens[i],
                    tokens[i - 1].uniBalanceOf(address(this))
                );
            } else if (flags[i - 1] == FLAG.V2_EXACT_IN) {
                _swapOnV2ExactIn(
                    tokens[i - 1],
                    tokens[i],
                    tokens[i - 1].uniBalanceOf(address(this))
                );
            }
        }

        returnAmount = dstToken.uniBalanceOf(address(this));
        require(
            returnAmount >= minReturn,
            "swapMulti: return amount is less than minReturn"
        );
        uint256 inRefund = srcToken.uniBalanceOf(address(this));


        uint256 userBalanceBefore = dstToken.uniBalanceOf(msg.sender);
        dstToken.uniTransfer(payable(msg.sender), returnAmount);
        require(
            dstToken.uniBalanceOf(msg.sender) - userBalanceBefore >= minReturn,
            "swapMulti: incorrect user balance"
        );

        srcToken.uniTransfer(payable(msg.sender), inRefund);
    }

    function swap(
        IERC20 srcToken,
        IERC20 dstToken,
        uint256 amount,
        uint256 minReturn,
        FLAG flag
    ) public payable nonReentrant returns (uint256 returnAmount) {


        if (srcToken == dstToken) {
            return amount;
        }

        // отвечает за перевод токенов с нашего кошелька на адрес контракта
        srcToken.uniTransferFrom(payable(msg.sender), address(this), amount);


        uint256 receivedAmount = srcToken.uniBalanceOf(address(this));

        if (flag == 0) {
            _swapOnStableSwap(srcToken, dstToken, receivedAmount);
        } else if (flag == 1) {
            _swapOnV2ExactIn(srcToken, dstToken, receivedAmount);
        }

        returnAmount = dstToken.uniBalanceOf(address(this));

        require(
            returnAmount >= minReturn,
            "swap: return amount is less than minReturn"
        );
        uint256 inRefund = srcToken.uniBalanceOf(address(this));
        emit Swap(
            msg.sender,
            address(srcToken),
            address(dstToken),
            receivedAmount - inRefund
        );

        uint256 userBalanceBefore = dstToken.uniBalanceOf(msg.sender);
        dstToken.uniTransfer(payable(msg.sender), returnAmount);
        require(
            dstToken.uniBalanceOf(msg.sender) - userBalanceBefore >= minReturn,
            "swap: incorrect user balance"
        );

        srcToken.uniTransfer(payable(msg.sender), inRefund);
    }

    // Swap helpers

    function _swapOnStableSwap(
        IERC20 srcToken,
        IERC20 dstToken,
        uint256 amount
    ) internal {
        require(
            stableswapFactory != address(0),
            "StableSwap factory cannot be zero address"
        );

        if (srcToken.isETH()) {
            weth.deposit{value: amount}();
        }

        IERC20 srcTokenReal = srcToken.isETH() ? weth : srcToken;
        IERC20 dstTokenReal = dstToken.isETH() ? weth : dstToken;

        IStableSwapFactory.StableSwapPairInfo memory info = IStableSwapFactory(
            stableswapFactory
        ).getPairInfo(address(srcTokenReal), address(dstTokenReal));

        if (info.swapContract == address(0)) {
            return;
        }

        IStableSwap stableSwap = IStableSwap(info.swapContract);
        IERC20[] memory tokens = new IERC20[](2);
        tokens[0] = IERC20(stableSwap.coins(uint256(0)));
        tokens[1] = IERC20(stableSwap.coins(uint256(1)));
        uint256 i = (srcTokenReal == tokens[0] ? 1 : 0) +
            (srcTokenReal == tokens[1] ? 2 : 0);
        uint256 j = (dstTokenReal == tokens[0] ? 1 : 0) +
            (dstTokenReal == tokens[1] ? 2 : 0);
        srcTokenReal.uniApprove(address(stableSwap), amount);
        stableSwap.exchange(i - 1, j - 1, amount, 0);

        if (dstToken.isETH()) {
            weth.withdraw(weth.balanceOf(address(this)));
        }
    }

    function _swapOnV2ExactIn(
        IERC20 srcToken,
        IERC20 dstToken,
        uint256 amount
    ) internal returns (uint256 returnAmount) {

        if (srcToken.isETH()) {
            weth.deposit{value: amount}();
        }

        IERC20 srcTokenReal = srcToken.isETH() ? weth : srcToken;
        IERC20 dstTokenReal = dstToken.isETH() ? weth : dstToken;

        IArbswapV2Exchange exchange = IArbswapV2Factory(arbswapV2).getPair(
            srcTokenReal,
            dstTokenReal
        );

        srcTokenReal.safeTransfer(address(exchange), amount);


        bool needSync;


        (returnAmount, needSync) = exchange.getReturn(
            srcTokenReal,
            dstTokenReal,
            amount
        );
        if (needSync) {
            exchange.sync();
        }

        if (srcTokenReal < dstTokenReal) {
            exchange.swap(0, returnAmount, address(this), "");
        } else {
            exchange.swap(returnAmount, 0, address(this), "");
        }

        if (dstToken.isETH()) {
            weth.withdraw(weth.balanceOf(address(this)));
        }
    }
}
