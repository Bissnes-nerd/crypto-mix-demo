
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BasicMixer {
    mapping(bytes32 => uint256) public deposits;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function deposit(bytes32 secretHash) public payable {
        require(msg.value > 0.01 ether, "Minimum deposit required");
        deposits[secretHash] = msg.value;
    }

    function withdraw(uint256 secret, address payable recipient) public {
        bytes32 hash = keccak256(abi.encodePacked(secret));
        uint256 amount = deposits[hash];
        require(amount > 0, "No funds found for secret");
        deposits[hash] = 0;
        recipient.transfer(amount);
    }

    receive() external payable {}
}
