import mlflow
import os

# 1. Force the URI inside the script to override any ENV variables
mlflow.set_tracking_uri("http://192.168.49.2:30758")

# 2. Use a completely unique name to force a fresh ID lookup
experiment_name = "Kidney_Success_Final"

try:
    # Try to find the experiment on the server
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        # Create it if it doesn't exist; this will give us a FRESH ID (e.g., 2, 3, or 4)
        experiment_id = mlflow.create_experiment(experiment_name)
    else:
        experiment_id = experiment.experiment_id
    
    # Set the active experiment explicitly by the ID we just fetched
    mlflow.set_experiment(experiment_id=experiment_id)
    print(f"Connected to MLflow. Using Experiment ID: {experiment_id}")

except Exception as e:
    print(f"MLflow Setup Error: {e}")

def train():
    # This will now use the specific experiment_id we found/created above
    with mlflow.start_run():
        # ... your training code ...
        print("Training started...")