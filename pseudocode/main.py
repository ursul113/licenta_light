from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db_handler
from core.executor2 import execute

app = Flask(__name__)
db=db_handler()
CORS(app, origins=["http://frontend:5173", "http://localhost:5173"])
@app.route('/process', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        pseudocode = data.get('pseudocode', '')
        keyboard_input = data.get('input', '')
        if not pseudocode:
            return jsonify({'error': 'Pseudocode is required!'}), 400
        result = execute(pseudocode,keyboard_input)

        return jsonify({
            'message': 'Code executed successfully!',
            'result': result
        }), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/save', methods=['POST'])
def save_code():
    data = request.get_json()
    name = data.get('name')
    code = data.get('code')
    if not name or not code:
        return jsonify({'error': 'Name and code are required'}), 400
    try:
        db.insert_run(name, code)
        return jsonify({'message': 'Saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load/<name>', methods=['GET'])
def load_code(name):
    try:
        result = db.get_code(name)
        if not result:
            return jsonify({'error': 'Code not found'}), 404
        return jsonify({'code': result[0][0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load_names', methods=['GET'])
def list_names():
    try:
        names = db.get_names()
        flat_names = [n[0] for n in names]
        return jsonify({'names': flat_names}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def main():
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
