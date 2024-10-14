// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IStableSwapFactory {
    struct StableSwapPairInfo {
        address swapContract;
        address token0;
        address token1;
        address LPContract;
    }

    // solium-disable-next-line mixedcase
    function pairLength() external view returns (uint256);

    // solium-disable-next-line mixedcase
    function getPairInfo(
        address _tokenA,
        address _tokenB
    ) external view returns (StableSwapPairInfo memory info);
}
