# train_crop_model.py
# This script trains a Decision Tree model to recommend crops based on district data.
# Updated to train on the full dataset for better performance with small data.

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def train_crop_recommender():
    """Trains and saves the crop recommendation model on the entire dataset."""
    # Load the dataset
    try:
        data = pd.read_csv('crop_recommendation_data.csv')
    except FileNotFoundError:
        print("Error: 'crop_recommendation_data.csv' not found.")
        print("Please make sure you have saved the dataset file in the same directory.")
        return

    # Prepare the data
    X = data[['district']]
    y = data['recommended_crop']

    # Encode categorical features and target variable
    X_encoded = pd.get_dummies(X, columns=['district'], drop_first=False) # Use drop_first=False to include all districts
    
    # Save the columns to apply them to new data
    model_columns = X_encoded.columns
    joblib.dump(model_columns, 'crop_model_columns.joblib')

    le_y = LabelEncoder()
    y_encoded = le_y.fit_transform(y)
    # Save the label encoder for decoding predictions later
    joblib.dump(le_y, 'crop_label_encoder.joblib')

    # --- Main Change: Train on the entire dataset ---
    # We are not splitting the data into train/test because the dataset is very small.
    # The goal is for the model to learn all the examples perfectly for the application.
    print("Training the crop recommendation model on the full dataset...")
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_encoded, y_encoded)
    print("Training complete.")

    # We can't calculate accuracy without a test set, which is fine for this use case.
    print("Model trained successfully on all available data.")

    # Save the trained model
    joblib.dump(model, 'crop_recommender_model.joblib')
    print("Model saved as 'crop_recommender_model.joblib'")
    print("Associated files 'crop_model_columns.joblib' and 'crop_label_encoder.joblib' also saved.")


if __name__ == '__main__':
    train_crop_recommender()