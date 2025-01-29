/// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../src/Token.sol"; // Importing the Token contract from the src folder

contract TokenTest is Test {
    Token token;

    // This function will run before each test
    function setUp() public {
        // Deploy a new Token contract before each test
        token = new Token("Test Token", "TST", 1000 ether, 18);
    }

    // Test initial supply
    function testInitialSupply() public {
        assertEq(token.totalSupply(), 1000 ether);
    }

    // Test decimals
    function testDecimals() public {
        assertEq(token.decimals(), 18);
    }

    // Test safeTransfer
    function testSafeTransfer() public {
        address recipient = address(0x123);
        uint256 amount = 100 ether;

        // Perform the transfer using the safeTransfer function
        token.safeTransfer(recipient, amount);

        // Verify the recipient received the correct amount
        assertEq(token.balanceOf(recipient), amount);
    }
}
