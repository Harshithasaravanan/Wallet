// SPDX-License-Identifier: UNLICENSED
/**pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20{
    uint8 private _decimals;
    constructor(string memory name, string memory ticker, uint initialBalance, uint8 __decimals) ERC20(name, ticker){
        _mint(msg.sender,initialBalance);
        _decimals = __decimals;
    }
    function decimals() public view override returns(uint8) {
        return _decimals;
    }

}**/

pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20 {
    uint8 private _dec;

    bool private _inTrans;

    constructor(string memory name, string memory ticker, uint initialBalance, uint8 __decimals) 
        ERC20(name, ticker) 
    {
        _mint(msg.sender, initialBalance);
        _dec = __decimals;
        _inTrans = false;
    }

    function decimals() public view override returns (uint8) {
        return _dec;
    }

    function safeTransfer(address recipient, uint256 amount) public returns (bool) {
        // Ensure no reentrancy by setting the lock
        require(!_inTrans, "ReentrancyGuard: reentrant call");
        _inTrans = true;

        bool success = super.transfer(recipient, amount);

        _inTrans = false;

        return success;
    }

    function safeMint(address account, uint256 amount) public returns (bool) {
        require(!_inTrans, "ReentrancyGuard: reentrant call");
        _inTrans = true;

        _mint(account, amount);

        _inTrans = false;
        return true;
    }
}
