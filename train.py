import mlflow
import mlflow.keras
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Internal Kubernetes DNS for MLflow
TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow.mlflow.svc.cluster.local:5000")
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment("Kidney_Scan_Classification")

def train():
    # Load photos from mounted volume /mnt/data
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    train_gen = datagen.flow_from_directory(
        '/mnt/data', target_size=(224, 224), batch_size=32, class_mode='binary', subset='training'
    )

    with mlflow.start_run():
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        
        # Training
        model.fit(train_gen, epochs=2)
        
        # Log to MLflow
        mlflow.keras.log_model(model, "kidney_model")
        print("Done! Model saved to MLflow.")

if __name__ == "__main__":
    train()