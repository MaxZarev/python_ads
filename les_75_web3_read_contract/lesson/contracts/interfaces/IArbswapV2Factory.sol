// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./IArbswapV2Exchange.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IArbswapV2Factory {
    function getPair(
        IERC20 tokenA,
        IERC20 tokenB
    ) external view returns (IArbswapV2Exchange pair);
}
