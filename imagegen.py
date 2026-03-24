from flask import Flask, render_template, request
import requests
import base64
import io

app = Flask(__name__)

import os # Add this at the very top of your file (Line 1)
from dotenv import load_dotenv # Add this import for loading environment variables
load_dotenv() # Load environment variables from .env file
# Securely get the token from the system environment
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
token = os.getenv("HF_TOKEN") 
HEADERS = {"Authorization": f"Bearer {token}"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_prompt = request.form['prompt']
    payload = {"inputs": user_prompt}
    
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        # Convert image bytes to a format HTML can understand (Base64)
        encoded_image = base64.b64encode(response.content).decode('utf-8')
        image_url = f"data:image/png;base64,{encoded_image}"
        return render_template('index.html', image_url=image_url)
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__== '__main__':
    app.run(debug=True)