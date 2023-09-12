import os
import unicodedata
import uuid

from bardapi import Bard
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, request, jsonify

app: Flask = Flask(__name__)
load_dotenv()


def generate_unique_session_id():
    return str(uuid.uuid4())


user_messages = []


@app.route('/', methods=['GET', 'POST'])
def get_bard_answer():
    if request.method == 'GET':
        return "Welcome bard api"
    elif request.method == 'POST':
        request_data = request.get_json(force=True)
        if not request_data or 'message' not in request_data:
            return jsonify({"error": "Please Write valid message in JSON format."}), 400

        message = request_data['message']

        user_messages.append(message)

        latest_user_message = user_messages[-1]

        bard_instance = Bard()
        bard_response = bard_instance.get_answer(str(latest_user_message))

        cleaned_bard_response = BeautifulSoup(bard_response['content'], 'html.parser').get_text()
        cleaned_bard_response = ''.join(c for c in cleaned_bard_response if unicodedata.category(c) != 'Mn')
        enhanced_bard_response = enhance_response(cleaned_bard_response)

        return jsonify({"responseText": enhanced_bard_response}), 200, {
            'Content-Type': 'application/json; charset=utf-8'}


def clean_response_text(text):
    cleaned_text = text.replace("\n", "").replace("\r", "").replace("*", " ")

    cleaned_text = BeautifulSoup(cleaned_text, 'html.parser').get_text()
    cleaned_text = ''.join(c for c in cleaned_text if unicodedata.category(c) != 'Mn')
    return cleaned_text


def enhance_response(enhanced_text):
    enhanced_text = enhanced_text.replace(".\r\n\r\n", ". ")
    enhanced_text = enhanced_text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").replace("*", " ")

    return enhanced_text


if __name__ == '__main__':
    app.run(port=5000)  # run app in debug mode on port 5001
