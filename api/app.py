

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__, static_folder='../static') 
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@app.route('/')
def index():
    return send_from_directory('../static', 'index.html')

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.json
    text_to_summarize = data.get('text')
    summary = summarize_with_groq_api(text_to_summarize)
    return jsonify({"summary": summary})

def summarize_with_groq_api(text):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": f"Summarize the following text: {text}"}
            ],
            model="llama3-8b-8192"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"
