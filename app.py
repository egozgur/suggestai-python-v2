from bardapi import Bard
import os
from flask import Flask, request, jsonify

os.environ["_BARD_API_KEY"] = "ZAgZWAtOoAgSTpgxQ-rfcSegvBGXEdArOgoOnfkbQb641XRK7raXqxqAgIRVD5k-vwvvYw."

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_bard_answer():
    if request.method == 'GET':
        return "Wellcome bard api"
    elif request.method == 'POST':
        data = request.get_json(force=True)
        if not data or 'message' not in data:
            return jsonify({"error": "Please Write valid Question in JSON format."}), 400

        message = data['message']
        bard_instance = Bard()
        response = bard_instance.get_answer(str(message))
        return jsonify(response['content'])


if __name__ == '__main__':
    app.run(port=5001)
