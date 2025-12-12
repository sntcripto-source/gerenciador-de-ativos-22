#!/usr/bin/env python3
"""
Flask server for Asset Manager - Provides REST API for data persistence
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Data file path
DATA_FILE = 'data.json'

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {DATA_FILE} is corrupted, returning empty data")
            return {}
    return {}

def save_data(data):
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', path)

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get all saved data"""
    try:
        data = load_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data', methods=['POST'])
def post_data():
    """Save data received from client"""
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'No data provided'}), 400
        
        if save_data(data):
            return jsonify({'success': True, 'message': 'Data saved successfully'}), 200
        else:
            return jsonify({'error': 'Failed to save data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Asset Manager Server")
    print("=" * 60)
    print(f"Server running at: http://localhost:5000")
    print(f"Data file: {os.path.abspath(DATA_FILE)}")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
