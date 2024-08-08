from flask import Flask, jsonify
from google.cloud import firestore
from datetime import datetime
import pytz
import os

app = Flask(__name__)

# Set up Firestore client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sample-af3bd-firebase-adminsdk-bw5ts-c19d4dda69.json'
db = firestore.Client()

@app.route('/', methods=['GET'])
def check_timestamps():
    collection_name = "tTime"
    
    if not collection_name:
        return jsonify({"error": "Collection name must be provided"}), 400

    try:
        # Get all documents in the collection
        collection_ref = db.collection(collection_name)
        docs = collection_ref.stream()

        current_time = datetime.now(pytz.utc)
        results = []

        for doc in docs:
            doc_data = doc.to_dict()
            timestamp = doc_data.get('tSetTimeLimit')

            if not timestamp:
                continue
            # Compare timestamp with current time
            results.append({"id": doc.id, "timestamp": timestamp.isoformat(), "is_future": timestamp > current_time})

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)