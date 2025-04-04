from web3 import Web3
import json

# Load ABI
with open("AuthContract_abi.json", "r") as f:
    abi = json.load(f)

# Load contract address
with open("contract_address.txt", "r") as f:
    contract_address = f.read().strip()

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Replace with the SAME address & private key used during deployment
my_address = web3.eth.accounts[0]
private_key = "0xb247dab77913d979915be784d263231fcd7bacf0a5a4e4d29026ab021368469d"

# Load the contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

def store_cid(uid, cid):
    nonce = web3.eth.get_transaction_count(my_address)
    tx = contract.functions.storeCID(uid, cid).build_transaction({
        'chainId': 1337,
        'gas': 6721975,
        'gasPrice': web3.to_wei('10', 'gwei'),
        'nonce': nonce,
        'from': my_address
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ Stored on-chain: UID = {uid}, CID = {cid}")
    return receipt

def get_cid(uid):
    try:
        cid = contract.functions.getCID(uid).call()
        print(f"📦 Retrieved from blockchain: {cid}")
        return cid
    except Exception as e:
        print("❌ Error:", str(e))
        return None
