# train_disease_model.py
# This script trains a CNN model to classify plant diseases from images.

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import os
import requests
import zipfile
import matplotlib.pyplot as plt

def find_image_directory(root_path):
    """
    Finds the correct image directory within the extracted folder by looking for the
    directory with the most subdirectories (which correspond to the classes).
    """
    print(f"Searching for image directory in: {root_path}")
    best_path = None
    max_subdirs = 0

    for dirpath, dirnames, filenames in os.walk(root_path):
        # The main image folder will contain many subdirectories (the classes).
        # We check for more than 10 as a heuristic.
        if len(dirnames) > max_subdirs and len(dirnames) > 10:
            # A common pattern in this dataset's class folders is '___'.
            is_class_folder = any('___' in d for d in dirnames)
            if is_class_folder:
                max_subdirs = len(dirnames)
                best_path = dirpath
    
    if best_path:
        print(f"Found image directory with {max_subdirs} classes: {best_path}")
    else:
        print(f"Could not automatically find the image directory inside '{root_path}'. Please check the folder structure manually.")

    return best_path


def download_and_extract_dataset():
    """Downloads and extracts the PlantVillage dataset."""
    dataset_url = "https://data.mendeley.com/public-files/datasets/tywbtsjrjv/files/d5652a28-c1d8-4b76-97f3-72fb80f94efc/file_downloaded"
    zip_path = "plantvillage.zip"
    extract_path = "plantvillage_dataset"

    if not os.path.exists(extract_path):
        print("Downloading PlantVillage dataset...")
        try:
            r = requests.get(dataset_url, stream=True)
            with open(zip_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print("Download complete.")

            print("Extracting dataset...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            print("Extraction complete.")
            os.remove(zip_path)
        except Exception as e:
            print(f"An error occurred during download or extraction: {e}")
            return None
    else:
        print("Dataset already exists.")

    # Find the correct directory containing the class folders
    image_dir = find_image_directory(extract_path)
    return image_dir


def create_model(num_classes):
    """Creates a CNN model using transfer learning with MobileNetV2."""
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    # Freeze the base model
    base_model.trainable = False

    # Add custom layers
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model

def train_model():
    """Trains the plant disease diagnosis model."""
    image_dir = download_and_extract_dataset()
    if image_dir is None:
        return

    # Image dimensions
    img_width, img_height = 224, 224
    batch_size = 32

    # Data augmentation and normalization for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2) # 20% of data for validation

    # Data generator for training
    train_generator = train_datagen.flow_from_directory(
        image_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training')

    # Data generator for validation
    validation_generator = train_datagen.flow_from_directory(
        image_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation')

    num_classes = len(train_generator.class_indices)
    print(f"Found {num_classes} classes.")

    model = create_model(num_classes)

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    epochs = 10
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // batch_size,
        epochs=epochs)

    # Save the trained model
    model.save('plant_disease_model.h5')
    print("Model saved as plant_disease_model.h5")

    # Save class indices
    import json
    with open('class_indices.json', 'w') as f:
        json.dump(train_generator.class_indices, f)
    print("Class indices saved as class_indices.json")

    # Plot training history
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()


if __name__ == '__main__':
    train_model()
