from flask import Blueprint, jsonify, request
from web3 import Web3
import json
import logging
from datetime import datetime

logs_bp = Blueprint('logs', __name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to Ganache CLI
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Contract address and ABI
contract_address = '0xdD000A4aAB57d172F26f0eB82Dd2b52CBdD1baC8'
with open('../blockchain/build/contracts/PhishingLog.json') as f:
    abi = json.load(f)['abi']

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)
# Get the default account from Ganache
default_account = web3.eth.accounts[0]

@logs_bp.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        logs = contract.functions.getLogs().call()
        # Ensure the logs are in a serializable format
        formatted_logs = [{'content': log[0], 'contentType': log[1], 'timestamp': log[2]} for log in logs]
        logger.info(f"Logs fetched successfully: {formatted_logs}")
        return jsonify(formatted_logs)
    except Exception as e:
        logger.error(f"Error fetching logs: {str(e)}")
        return jsonify({"error": str(e)}), 500

@logs_bp.route('/api/logs', methods=['POST'])
def add_log():
    data = request.json
    if data:
        try:
            timestamp_str = data.get('timestamp')
            timestamp = int(datetime.fromisoformat(timestamp_str).timestamp())
            tx_hash = contract.functions.addLog(data['content'], data['contentType'], timestamp).transact({'from': default_account})
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            # Convert the receipt to a JSON-serializable format
            receipt_dict = {
                'transactionHash': receipt['transactionHash'].hex(),
                'blockHash': receipt['blockHash'].hex(),
                'blockNumber': receipt['blockNumber'],
                'contractAddress': receipt['contractAddress'],
                'cumulativeGasUsed': receipt['cumulativeGasUsed'],
                'from': receipt['from'],
                'gasUsed': receipt['gasUsed'],
                'logs': [dict(log) for log in receipt['logs']],
                'status': receipt['status'],
                'to': receipt['to'],
                'transactionIndex': receipt['transactionIndex']
            }
            logger.info(f"Transaction successful: {receipt_dict['transactionHash']}")
            return jsonify(receipt_dict), 201
        except Exception as e:
            logger.error(f"Error adding log: {str(e)}")
            return jsonify({"error": str(e)}), 500
    else:
        logger.warning("No data provided in the request")
        return jsonify({"message": "No data provided"}), 400
