from flask import Flask, request, jsonify
import joblib
import pandas as pd
from web3 import Web3
# from pymongo import MongoClient
import json
from datetime import datetime
from api.logs import logs_bp
from flask_cors import CORS
import re
app = Flask(__name__)
app.register_blueprint(logs_bp)
CORS(app)

model = joblib.load('models/phishing_model_best.pkl')

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
contract_address = '0xdD000A4aAB57d172F26f0eB82Dd2b52CBdD1baC8' 
with open('../blockchain/build/contracts/PhishingLog.json') as f:
    abi = json.load(f)['abi']

contract = w3.eth.contract(address=contract_address, abi=abi)


# mongo_client = MongoClient('mongodb://localhost:27017/')
# db = mongo_client['phishing_detection']  
# logs_collection = db['logs']  


if not w3.eth.default_account:
    w3.eth.default_account = w3.eth.accounts[0]

def extract_features(df, type_):
    features = pd.DataFrame()
    if type_ == 'email':
        features['length'] = df['email_text'].apply(len)
      
    elif type_ == 'url':
        features['length'] = df['url'].apply(len)
        features['num_dots'] = df['url'].apply(lambda x: x.count('.'))
        features['has_ip'] = df['url'].apply(lambda x: bool(re.search(r'\d+\.\d+\.\d+\.\d+', x)))
    return features
@app.route('/api/logs', methods=['POST'])
def add_log():
    data = request.json
    content = data.get('content')
    content_type = data.get('contentType')
    timestamp_str = data.get('timestamp')

    if content_type not in ['phishing_url', 'phishing_email']:
        return jsonify({"error": "Invalid content type"}), 400

    if not content or not timestamp_str:
        return jsonify({"error": "Content and timestamp are required"}), 400

    try:
        timestamp = int(datetime.fromisoformat(timestamp_str).timestamp())
        print("Parsed timestamp:", timestamp)
    except ValueError:
        return jsonify({"error": "Invalid timestamp format"}), 400

    try:
        df = pd.DataFrame([{'email_text': content}] if content_type == 'phishing_email' else [{'url': content}])
        features = extract_features(df, 'email' if content_type == 'phishing_email' else 'url')
        print("Extracted features:", features)
        prediction = model.predict(features)
        print("Prediction:", prediction)
        is_phishing = prediction[0] == 1
    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500

    try:
        tx_hash = contract.functions.addLog(content, content_type, timestamp).transact({
            'from': w3.eth.default_account
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        tx_hash_hex = tx_hash.hex()
        receipt_dict = dict(receipt)
        receipt_dict['transactionHash'] = tx_hash_hex

        return jsonify({
            "type": content_type,
            "content": content,
            "timestamp": timestamp,
            "is_phishing": int(is_phishing),
            "transaction_receipt": receipt_dict
        })
    except Exception as e:
        print("Blockchain interaction error:", e)
        return jsonify({"error": f"Blockchain interaction error: {str(e)}"}), 500
