from web3 import Web3
from solcx import compile_standard, install_solc
import json
import os

# Ensure Solidity compiler is available
install_solc("0.8.0")

# Read Solidity source code
with open("AuthContract.sol", "r") as f:
    source_code = f.read()

# Compile contract
compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {"AuthContract.sol": {"content": source_code}},
        "settings": {
            "outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}
        },
    },
    solc_version="0.8.0",
)

# Extract ABI and Bytecode
abi = compiled["contracts"]["AuthContract.sol"]["AuthContract"]["abi"]
bytecode = compiled["contracts"]["AuthContract.sol"]["AuthContract"]["evm"]["bytecode"]["object"]

# Save ABI
with open("AuthContract_abi.json", "w") as f:
    json.dump(abi, f)

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Set your account
my_address = web3.eth.accounts[0]
private_key = "0xb247dab77913d979915be784d263231fcd7bacf0a5a4e4d29026ab021368469d"  # ⚠️ Replace securely from Ganache

# Create contract object
AuthContract = web3.eth.contract(abi=abi, bytecode=bytecode)

# Get nonce
nonce = web3.eth.get_transaction_count(my_address)

# Build transaction
tx = AuthContract.constructor().build_transaction({
    "chainId": 1337,
    "from": my_address,
    "nonce": nonce,
    "gas": 6721975,
    "gasPrice": web3.to_wei("10", "gwei"),
})

# Sign and send
signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# Save contract address
with open("contract_address.txt", "w") as f:
    f.write(tx_receipt.contractAddress)

print("✅ Contract deployed at:", tx_receipt.contractAddress)
