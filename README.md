# Kidney-Disease-MLFlow-Model


Kidney Disease Classification with MLflow & Kubernetes
1. Project Overview

This repository contains a Deep Learning pipeline for Kidney CT scan classification.

    Model: CNN (TensorFlow/Keras)

    Tracking: MLflow (hosted on Kubernetes)

    Environment: Minikube

2. MLflow Infrastructure Setup

The MLflow server acts as a central hub for all training metrics, parameters, and model versions.
Step 1: Deploy MLflow to Minikube

We deploy MLflow using a NodePort service to make the UI accessible from the host machine.
Bash

kubectl create namespace mlflow
kubectl apply -f k8s/mlflow-deployment.yaml -n mlflow

Step 2: Identify the Tracking URI

MLflow requires a specific URI to receive data.

    External (Your Browser/Local Script): Use http://<minikube-ip>:<node-port>

    Internal (Inside K8s Pods): Use http://mlflow.mlflow.svc.cluster.local:80

Step 3: Access the Dashboard

Run minikube ip and kubectl get svc -n mlflow to find your coordinates.
Example: http://192.168.49.2:30758
3. Data & Permissions Strategy
Step 1: Reclaim Folder Ownership

If you encounter Permission Denied errors during git pull or file access, reset ownership:
Bash

sudo chown -R $USER:$USER .

Step 2: Mount Training Data

MLflow needs data to train. Mount your local dataset into the Minikube VM so the cluster can see it:
Bash

minikube mount $(pwd)/data:/mnt/data

Note: Keep this terminal window open during training.
4. Executing the MLflow Experiment
Context: Handling Ephemeral Storage

By default, this setup uses sqlite:///:memory:. If the MLflow pod restarts, all previous experiment IDs are lost. To prevent RESOURCE_DOES_NOT_EXIST errors, always fetch the Experiment ID by Name in your script.
Running the Training Script

    Install Dependencies: pip install tensorflow mlflow

    Execute:

Bash

# Point to your Minikube MLflow instance
export MLFLOW_TRACKING_URI="http://$(minikube ip):30758"

# Force a fresh experiment name to avoid ID conflicts
export MLFLOW_EXPERIMENT_NAME="Kidney_Scan_Run_$(date +%Y%m%d)"

python3 train.py


# Kubernetes Orchestration (k8s)

In a production-like flow, we don't run docker run manually. We use Kubernetes Jobs to handle the training logic. A Job is ideal for ML because it runs until the training is finished and then stops, releasing resources.
Step 1: Build the Image for the Cluster

Before K8s can run your code, the image must be available to the Minikube nodes.
Bash

# Point your terminal to Minikube's Docker daemon
eval $(minikube docker-env)

# Build the trainer image
docker build -t kidney-trainer:latest -f docker/Dockerfile .

Step 2: Configure the Job Manifest

Ensure your k8s/job.yaml points to the internal Service DNS. This allows the Training Pod to find the MLflow Pod across the cluster.

File: k8s/job.yaml (Key Snippet)
YAML

spec:
  template:
    spec:
      containers:
      - name: trainer
        image: kidney-trainer:latest
        imagePullPolicy: Never  # Vital: tells K8s to use the image we just built locally
        env:
        - name: MLFLOW_TRACKING_URI
          value: "http://mlflow.mlflow.svc.cluster.local:80"
        volumeMounts:
        - name: data-vol
          mountPath: /mnt/data
      volumes:
      - name: data-vol
        hostPath:
          path: /home/saurabhbhale/kra/Kidney-Disease-MLFlow-Model/data

Step 3: Deploy the Training Job

Run the job in the same namespace as MLflow to simplify networking.
Bash

kubectl apply -f k8s/job.yaml -n mlflow

5. Reviewing Results in MLflow




    
