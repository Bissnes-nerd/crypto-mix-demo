
# Ethereum Crypto Mixer Project

## Structure

- contracts/BasicMixer.sol: Solidity smart contract
- backend/app.py: Flask server with Web3.py
- backend/contract_abi.json: ABI for contract interaction

## How to Run

### Prerequisites
- Ganache for local Ethereum
- Python 3 + Flask + Web3.py
- MetaMask or another wallet

### Steps

1. Deploy `BasicMixer.sol` using Remix or Hardhat to Ganache
2. Copy contract address into `backend/app.py`
3. Replace `"0xYourPrivateKeyHere"` with your Ganache account private key
4. Place contract ABI into `contract_abi.json`
5. Run:
   ```bash
   cd backend
   python3 app.py
   ```
6. Use Postman or cURL to:
   - `POST /start` with body:
     ```json
     {
       "outputs": [
         {"address": "0xRecipient1"},
         {"address": "0xRecipient2"}
       ]
     }
     ```
   - `GET /check/<hash>`

## Notes

This is for educational/demonstration use only.
