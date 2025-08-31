🌿 Agri-Sage AI (CS7050NI Coursework)
This repository contains the source code for Agri-Sage AI, an intelligent agent for plant disease diagnosis, built for the Artificial Intelligence module (CS7050NI). The agent integrates a local Convolutional Neural Network (CNN) for core analysis with the Google Gemini API for a fully conversational user experience.

✨ Key Features
Intelligent Agent Architecture: Built on the foundational Sense-Think-Act cycle.

Hybrid AI System: Integrates two distinct AI models: a local CNN for visual recognition and a cloud-based LLM for natural language interaction.

Conversational UI: A modern, chat-based interface allows for intuitive interaction, including follow-up questions.

Robust & Resilient: Features a graceful degradation mechanism that allows the core diagnosis to function even if the external Gemini API is unavailable.

🚀 Setup and Running Instructions
Follow these steps precisely to set up and run the project locally.

1. Initial Setup
If you have downloaded the source code as a ZIP, unzip it. Otherwise, clone the repository from GitHub:

git clone [https://github.com/BhabishyaLuitel/agri-sage-ai.git](https://github.com/BhabishyaLuitel/agri-sage-ai.git)
cd agri-sage-ai

2. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

For Windows:

python -m venv venv
venv\Scripts\activate

For macOS/Linux:

python3 -m venv venv
source venv/bin/activate

You should now see (venv) at the beginning of your terminal prompt.

3. Install Dependencies
A requirements.txt file is provided, which lists all the necessary Python libraries. Install them using pip:

pip install -r requirements.txt

4. Set Up Environment Variables (Crucial Step)
This project requires a Google Gemini API key to power its conversational features. This key must be stored securely.

In the root of the project folder, create a new file named exactly .env.

Inside this .env file, add your personal API key in the following format (replace your_actual_api_key_here with your key):

GEMINI_API_KEY=your_actual_api_key_here

5. Generate the Machine Learning Model
The trained CNN model (plant_disease_model.h5) is not included in the repository due to its large size. You must generate it by running the training script. This script will also download the required PlantVillage image dataset.

Note: This process is computationally intensive and will take a significant amount of time.

python train_disease_model.py

After the script finishes, you will have the plant_disease_model.h5 and class_indices.json files in your project directory.

6. Run the Application
Once the model has been trained and the setup is complete, you can start the Flask web server with the following command:

python app.py

The application will now be running. Open your web browser and navigate to the following address to interact with the Agri-Sage AI agent:

http://127.0.0.1:5000