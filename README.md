Agri-Sage AI (CS7050NI Coursework)
This is a prototype of an intelligent agent for plant disease diagnosis, built for the Artificial Intelligence module (CS7050NI). The agent integrates a local Convolutional Neural Network (CNN) for diagnosis with the Google Gemini API for a fully conversational user experience.

Setup and Running Instructions
Follow these steps precisely to set up and run the project.

1. Clone the Repository
If you have downloaded the source code as a ZIP, you can skip this step. Otherwise, clone the repository from GitHub:

git clone [https://github.com/your-username/agri-sage-ai.git](https://github.com/your-username/agri-sage-ai.git)
cd agri-sage-ai

2. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

You should see (venv) at the beginning of your terminal prompt.

3. Install Dependencies
A requirements.txt file is provided, which lists all the necessary Python libraries. Install them using pip:

pip install -r requirements.txt

4. Set Up Environment Variables (Crucial Step)
This project requires a Google Gemini API key to power its conversational features. This key must be stored securely and should never be committed to version control.

In the root of the project folder, create a new file named exactly .env.

Inside this .env file, add your personal API key in the following format (replace your_actual_api_key_here with your key):

GEMINI_API_KEY=your_actual_api_key_here

5. Generate the Machine Learning Model
The trained CNN model (plant_disease_model.h5) is not included in the source code due to its large size. You must generate it by running the training script. This script will also download the required PlantVillage image dataset.

Note: This process is computationally intensive and will take a significant amount of time.

python train_disease_model.py

After the script finishes, you will have the plant_disease_model.h5 and class_indices.json files in your project directory.

6. Run the Application
Once the model has been trained and the setup is complete, you can start the Flask web server with the following command:

python app.py

The application will now be running. Open your web browser and navigate to the following address to interact with the Agri-Sage AI agent:

http://127.0.0.1:5000