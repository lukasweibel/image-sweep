import os

from flask import Flask, jsonify, send_from_directory
from flask import Response, request
from inference import predict_class

app = Flask(__name__, static_folder='./../frontend/public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/picture', methods=['POST'])
def classifyPicture():
    if 'picture' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['picture']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        predicted_class = predict_class(file)
        return jsonify({"message": "The file is classified as: " + predicted_class}), 200

    return jsonify({"error": "File upload failed"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=80)
