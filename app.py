from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file_to_adobe():
    try:
        adobe_url = request.json.get('adobe_url')
        file_path = request.json.get('file_path')

        if not adobe_url or not file_path:
            return jsonify({"error": "Missing 'adobe_url' or 'file_path'"}), 400

        with open(file_path, "rb") as file_data:
            headers = {"Content-Type": "application/pdf"}
            response = requests.put(adobe_url, data=file_data, headers=headers)
            response.raise_for_status()

        return jsonify({"status": "success", "response_headers": dict(response.headers)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
