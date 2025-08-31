# app.py
# Final version with a conversational Gemini-powered UI for the AI Coursework.
# Includes a fallback mechanism for demo stability if the Gemini API is unavailable.

import os
import json
import joblib
import numpy as np
import pandas as pd
from PIL import Image
from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import base64
from io import BytesIO
import requests
import time

# --- Initialization ---
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# --- Import Configuration ---
from config import GEMINI_API_KEY, GEMINI_MODEL

# --- Gemini API Configuration ---
API_KEY = GEMINI_API_KEY
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"

# --- Load Local Model ---
try:
    disease_model = load_model('plant_disease_model.h5')
    with open('class_indices.json', 'r') as f:
        class_indices = json.load(f)
    class_names = {v: k for k, v in class_indices.items()}
    print("✅ Disease diagnosis model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading local model: {e}")
    disease_model = None 

# --- Helper Functions ---
def preprocess_image(image, target_size=(224, 224)):
    """Preprocesses the image for the local CNN model."""
    img = Image.open(image).convert('RGB')
    img = img.resize(target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def image_to_base64(image):
    """Converts a file stream to a base64 string for embedding in the chat."""
    buffered = BytesIO()
    pil_image = Image.open(image)
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def predict_disease(image):
    """Runs the local disease diagnosis model."""
    if not disease_model: return "Model not loaded", 0.0
    processed_image = preprocess_image(image)
    predictions = disease_model.predict(processed_image)
    predicted_class_index = np.argmax(predictions[0])
    confidence = np.max(predictions[0])
    predicted_class_name = class_names.get(predicted_class_index, "Unknown")
    if "background" in predicted_class_name.lower():
        return "Could not identify a specific disease from this image.", 0.0
    return predicted_class_name.replace("_", " "), float(confidence)

# --- Gemini API Call with Fallback ---
def get_gemini_response(prompt):
    """Calls the Gemini API but returns None on failure instead of crashing."""
    if not API_KEY:
        print("⚠️ Gemini API key is missing. Operating in fallback mode.")
        return None
        
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    max_retries = 2 # Reduced for faster fallback
    delay = 1
    for attempt in range(max_retries):
        try:
            response = requests.post(GEMINI_API_URL, json=payload, headers={'Content-Type': 'application/json'}, timeout=15)
            response.raise_for_status()
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        except requests.exceptions.RequestException as e:
            print(f"API request failed (attempt {attempt + 1}): {e}")
            if e.response and e.response.status_code == 403:
                print("❌ Gemini API key is invalid. Operating in fallback mode.")
                return None
            time.sleep(delay)
            delay *= 2
    
    print("API connection failed after multiple retries. Operating in fallback mode.")
    return None # Return None on final failure

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message')
    uploaded_file = request.files.get('image')
    context_disease = request.form.get('context_disease') 
    
    if uploaded_file:
        # --- This is an analysis request ---
        disease_prediction, confidence = predict_disease(uploaded_file)
        uploaded_file.seek(0)
        image_b64 = image_to_base64(uploaded_file)
        
        prompt = f"You are Agri-Sage, a friendly AI agricultural advisor. Your local model diagnosed an image with: '{disease_prediction}' ({confidence:.1%} confidence). Present this result briefly. Then ask if the user wants treatment advice."
        gemini_response = get_gemini_response(prompt)
        
        # --- FALLBACK LOGIC ---
        if gemini_response is None:
            # If Gemini fails, create a simple, direct response.
            response_text = f"**Diagnosis Complete**\n\nMy analysis indicates this could be **{disease_prediction}** with a confidence of {confidence:.1%}.\n\n*(Note: Conversational features are temporarily unavailable.)*"
        else:
            response_text = gemini_response

        return jsonify({'response': response_text, 'image': image_b64, 'disease_name': disease_prediction})

    else:
        # --- This is a follow-up or casual chat message ---
        prompt = ""
        base_prompt = "You are Agri-Sage, a friendly and concise AI agricultural advisor for Nepal."
        treatment_keywords = ['treat', 'help', 'fix', 'cure', 'plan', 'advice']

        if context_disease and any(keyword in user_message.lower() for keyword in treatment_keywords):
            prompt = f"{base_prompt} A user was diagnosed with '{context_disease}' and is asking for help: \"{user_message}\". Provide a brief, bullet-point summary of treatment options."
        elif context_disease:
            prompt = f"{base_prompt} You were discussing '{context_disease}'. The user now says: \"{user_message}\". Respond helpfully and concisely."
        else:
            prompt = f"{base_prompt} A user just said: '{user_message}'. Respond in a brief, conversational manner."
        
        gemini_response = get_gemini_response(prompt)

        # --- FALLBACK LOGIC ---
        if gemini_response is None:
            response_text = "I'm sorry, my conversational features are currently unavailable. Please try again later."
        else:
            response_text = gemini_response
        
        return jsonify({'response': response_text, 'disease_name': context_disease})

if __name__ == '__main__':
    app.run(debug=True)

