import os
import unicodedata

from bardapi import Bard
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, request, jsonify

app = Flask(__name__)
load_dotenv()


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

        cleaned_response = clean_response_text(response['content'])
        return jsonify({"responseText": cleaned_response}), 200, {'Content-Type': 'application/json; charset=utf-8'}


def clean_response_text(text):
    cleaned_text = text.replace("\n", "").replace("\r", "")
    cleaned_text = BeautifulSoup(cleaned_text, 'html.parser').get_text()
    cleaned_text = ''.join(c for c in cleaned_text if unicodedata.category(c) != 'Mn')
    return cleaned_text


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
