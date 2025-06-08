from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file_to_adobe():
    try:
        adobe_url = request.json.get('adobe_url')
        file_base64 = request.json.get('file_base64')  # expect base64 content, not file_path

        if not adobe_url or not file_base64:
            return jsonify({"error": "Missing 'adobe_url' or 'file_base64'"}), 400

        # Decode base64 string to bytes
        file_bytes = base64.b64decode(file_base64)

        headers = {"Content-Type": "application/pdf"}
        response = requests.put(adobe_url, data=file_bytes, headers=headers)
        response.raise_for_status()

        return jsonify({"status": "success", "response_headers": dict(response.headers)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
