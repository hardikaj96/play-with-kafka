from flask import Flask, render_template, jsonify, request
import random
from datetime import datetime, timedelta
from mongo_client import get_mongodb_client_connection

app = Flask(__name__)

mongo_db_name = 'db'
mongo_collection_name = 'your_collection_name'

client = get_mongodb_client_connection()

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/')
def index():
    return render_template('index1.html')


@app.route('/api/data', methods=['GET'])
def get_data():
    latest_timestamp_str = request.args.get('latestTimestamp')
    
    if latest_timestamp_str:
        try:
            latest_timestamp = datetime.strptime(latest_timestamp_str, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return jsonify({'error': 'Invalid timestamp format'}), 400
    else:
        return jsonify({'error': 'Invalid'})
    try:
        db = client[mongo_db_name]
        collection = db[mongo_collection_name]
        documents = list(collection.find({'datetime': {'$gt': latest_timestamp}}, {'_id': 0}, sort=[('datetime', -1)], limit=15))
        documents = documents[::-1]
        if not documents:
            return jsonify({'documents': [], 'latest_timestamp': None})
        for doc in documents:
            doc['datetime'] = datetime.strptime(doc['datetime'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%dT%H:%M:%S.%f')
        return jsonify({'documents': documents, 'latest_timestamp': documents[0]['datetime']})
    except:
        return jsonify({'documents': [], 'latest_timestamp': None})

@app.route('/prepopulate', methods=['GET'])
def prepopulate_data():
    try:
        db = client[mongo_db_name]
        collection = db[mongo_collection_name]
        documents = list(collection.find({}, {'_id': 0}, sort=[('datetime', -1)], limit=15))
        if not documents:
            return jsonify({'documents': [], 'latest_timestamp': None})
        documents = documents[::-1]
        for doc in documents:
            doc['datetime'] = datetime.strptime(doc['datetime'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%dT%H:%M:%S.%f')
        return jsonify({'documents': documents, 'latest_timestamp': documents[-1]['datetime']})
    except:
        return jsonify({'documents': [], 'latest_timestamp': None})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
