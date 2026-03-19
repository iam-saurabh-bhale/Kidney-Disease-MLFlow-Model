Kidney Disease Classification with MLflow & Kubernetes
1. Project Overview

This repository contains a Deep Learning pipeline to classify kidney CT scans into Normal or Tumor categories.

    Model: CNN (TensorFlow/Keras)

    Tracking: MLflow (hosted on Kubernetes)

    Orchestration: Kubernetes Jobs & Helm

    Environment: Minikube

2. Infrastructure Setup (Choose One)
Option A: Standard Kubernetes Manifests

```

kubectl create namespace mlflow
kubectl apply -f k8s/mlflow-deployment.yaml -n mlflow
```

Option B: Helm (Recommended for Production)

Using Helm allows for easier lifecycle management of the MLflow stack.

```
Bash

helm repo add community-charts https://community-charts.github.io/helm-charts
helm repo update
```

# Install MLflow with NodePort enabled for local access
```
helm install mlflow community-charts/mlflow \
  --namespace mlflow \
  --set service.type=NodePort \
  --set service.nodePort=30758 \
  --set backendStore.type=sqlite
```
3. Data & Permissions Strategy
Step 1: Reclaim Folder Ownership

If you encounter Permission Denied errors (common after using sudo or docker), reset ownership:

```
sudo chown -R $USER:$USER .
```

Step 2: Mount Training Data to Minikube

Since K8s pods cannot see your local drive directly, mount your data folder into the Minikube VM:
Bash

# Run this in a separate terminal and keep it open

```
minikube mount $(pwd)/data:/mnt/data
```


4. Training Execution
Option A: Local Run (Directly on Laptop)

Ideal for rapid debugging before deploying to the cluster.

```
export MLFLOW_TRACKING_URI="http://$(minikube ip):30758"
export MLFLOW_EXPERIMENT_NAME="Kidney_Local_$(date +%Y%m%d)"
python3 train.py
```

Option B: Kubernetes Job (Cluster Execution)

Build the Image inside Minikube's Docker daemon:

   ```
   eval $(minikube docker-env)
    docker build -t kidney-trainer:latest -f docker/Dockerfile .

    Deploy the Job:
    Bash

    kubectl apply -f k8s/job.yaml -n mlflow
```

Note : I have taken the help from the Google Gemini and ChatGPT as code is having multiple issue in deployment. Also while trying to sort issue once common issue occured related to Dockerize model not able to locate the MLFlow resources.
<img width="889" height="91" alt="image" src="https://github.com/user-attachments/assets/6637d5e1-f257-461d-917a-67671962f11c" />
<img width="1343" height="999" alt="image" src="https://github.com/user-attachments/assets/fa89a454-dc64-4f91-94e2-87a2cb90deee" />

 <img width="1862" height="507" alt="image" src="https://github.com/user-attachments/assets/1c1b3a64-69cd-41c5-9c72-f6f2d009443c" /><img width="1233" height="442" alt="image" src="https://github.com/user-attachments/assets/c3f9a63c-466d-444b-864b-36f2a29f8584" />

