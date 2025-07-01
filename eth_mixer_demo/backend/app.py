
from flask import Flask, request, jsonify
from web3 import Web3
import json
import secrets
import time
import threading

app = Flask(__name__)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Ganache
with open("contract_abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)

contract_address = "0xYourContractAddressHere"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)
deposits = {}

@app.route("/start", methods=["POST"])
def start_mixing():
    data = request.get_json()
    secret = secrets.randbits(256)
    hashed = w3.keccak(hex(secret).encode()).hex()
    deposits[hashed] = {
        "secret": secret,
        "outputs": data["outputs"],
        "status": "waiting"
    }
    return jsonify({
        "secret_hash": hashed,
        "deposit_address": contract_address,
        "instructions": f"Send ETH to {contract_address} with secret hash {hashed}"
    })

@app.route("/check/<hash_id>", methods=["GET"])
def check_status(hash_id):
    return jsonify(deposits.get(hash_id, {"error": "not found"}))

def monitor_deposits():
    while True:
        for hashed, info in deposits.items():
            if info["status"] == "waiting":
                if contract.functions.deposits(hashed).call() > 0:
                    info["status"] = "mixing"
                    threading.Thread(target=process_withdrawals, args=(hashed, info)).start()
        time.sleep(10)

def process_withdrawals(hash_id, info):
    time.sleep(30)  # Simulate delay
    total = contract.functions.deposits(hash_id).call()
    secret = info["secret"]
    outputs = info["outputs"]
    sender = w3.eth.accounts[0]
    for out in outputs:
        tx = contract.functions.withdraw(secret, out["address"]).build_transaction({
            "from": sender,
            "gas": 200000,
            "gasPrice": w3.toWei("20", "gwei"),
            "nonce": w3.eth.get_transaction_count(sender)
        })
        signed = w3.eth.account.sign_transaction(tx, private_key="0xYourPrivateKeyHere")
        w3.eth.send_raw_transaction(signed.rawTransaction)
        time.sleep(10)
    info["status"] = "complete"

if __name__ == "__main__":
    threading.Thread(target=monitor_deposits, daemon=True).start()
    app.run(port=5000)
