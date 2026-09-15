# Flask Portfolio – CI/CD with Azure DevOps and AKS

This project demonstrates an end-to-end CI/CD pipeline for a Flask portfolio application.

The Flask application is containerized using Docker. Azure DevOps automatically builds a new Docker image when code is committed to the `main` branch, pushes the image to Docker Hub, and deploys the new version to Azure Kubernetes Service (AKS).

## CI/CD Architecture

```text
Code Change
    ↓
Azure Repos
    ↓
Azure DevOps Pipeline
    ↓
Build Docker Image
    ↓
Tag Image with Build ID
    ↓
Push Image to Docker Hub
    ↓
Deploy to Azure Kubernetes Service (AKS)
    ↓
Kubernetes Pods
    ↓
LoadBalancer Service
    ↓
Live Flask Portfolio
```

## Technologies Used

- Python
- Flask
- HTML / CSS
- MySQL
- Docker
- Docker Hub
- Kubernetes
- Azure Kubernetes Service (AKS)
- Azure DevOps
- Azure Repos
- Azure Pipelines

---

# 1. Flask Application

The application is a personal portfolio website developed using Python and Flask.

The Flask application runs on port:

```text
5000
```

The application contains portfolio information and uses MySQL as the database.

Important application files include:

```text
flask_app.py
requirements.txt
templates/
static/
```

---

# 2. Docker

The Flask application is packaged into a Docker container.

The `Dockerfile` contains the instructions required to create the Docker image.

Basic process:

```text
Flask source code
       ↓
Dockerfile
       ↓
Docker image
       ↓
Docker container
```

Docker allows the application and its dependencies to be packaged together so that the application runs consistently in different environments.

The Docker Hub repository used by this project is:

```text
priyadocker2025/flask-portfolio
```

---

# 3. Kubernetes

The containerized application is deployed to Azure Kubernetes Service (AKS).

The Kubernetes configuration files are:

```text
deployment.yaml
service.yaml
mysql.yaml
```

## deployment.yaml

`deployment.yaml` defines how the Flask application runs inside Kubernetes.

The deployment runs three replicas of the Flask application.

```text
Flask Deployment
      ↓
3 Flask Pods
```

Running multiple replicas provides availability and allows Kubernetes to manage the application containers.

The deployment also references the Docker Hub image.

Example:

```yaml
image: priyadocker2025/flask-portfolio:18
```

The image number changes when a new image is created by the CI/CD pipeline.

---

# 4. Kubernetes Service

`service.yaml` exposes the Flask application outside the Kubernetes cluster.

The service type is:

```text
LoadBalancer
```

The LoadBalancer provides an external IP address that can be used to access the portfolio application from a browser.

Check the service using:

```bash
kubectl get service -n flask-app
```

Example:

```text
NAME                      TYPE           EXTERNAL-IP
flask-portfolio-service   LoadBalancer   85.211.172.64
```

The application can then be accessed using the external IP.

---

# 5. Kubernetes Namespace

The project uses the namespace:

```text
flask-app
```

To check the running pods:

```bash
kubectl get pods -n flask-app
```

Expected result:

```text
flask-portfolio-xxxxx   1/1   Running
flask-portfolio-xxxxx   1/1   Running
flask-portfolio-xxxxx   1/1   Running
mysql-xxxxx             1/1   Running
```

There are three Flask application pods and one MySQL pod.

---

# 6. Docker Hub Authentication

The Docker Hub repository is private.

Therefore, Kubernetes requires authentication before it can pull the Flask Docker image.

The Kubernetes deployment uses:

```yaml
imagePullSecrets:
  - name: dockerhub-secret
```

The secret allows AKS to authenticate with Docker Hub and download the private image.

Without the secret, pods can fail with:

```text
ImagePullBackOff
```

or:

```text
pull access denied
```

To check the secret:

```bash
kubectl get secrets -n flask-app
```

---

# 7. Azure DevOps CI/CD Pipeline

The CI/CD pipeline is defined in:

```text
azure-pipelines.yml
```

The pipeline automatically runs when a change is committed to the `main` branch.

The pipeline contains two main stages:

```text
Stage 1: Build and Push
             ↓
Stage 2: Deploy to AKS
```

## Stage 1 – Build and Push

Azure DevOps:

1. Reads the source code from Azure Repos.
2. Uses the Dockerfile to build a Docker image.
3. Tags the image using the Azure DevOps Build ID.
4. Pushes the image to Docker Hub.

For example:

```text
priyadocker2025/flask-portfolio:18
```

Here:

```text
18 = Azure DevOps Build ID used as the image tag
```

Using a build-specific image tag makes it possible to identify which application version is deployed.

---

# 8. Deploy to AKS

After the Docker image has been successfully built and pushed, the deployment stage runs.

Azure DevOps connects to the AKS cluster and deploys the new Docker image.

The process is:

```text
Docker Hub
     ↓
New Docker Image
     ↓
Azure DevOps
     ↓
AKS Deployment
     ↓
New Kubernetes Pods
```

Kubernetes performs a rollout so the old application containers are replaced by containers running the new image.

---

# 9. Complete CI/CD Workflow

The complete workflow is:

```text
Developer changes application code
             ↓
Commit to main branch
             ↓
Azure DevOps pipeline automatically starts
             ↓
Docker image is built
             ↓
Image is tagged with Build ID
             ↓
Image is pushed to Docker Hub
             ↓
Deployment stage starts
             ↓
AKS pulls the new image
             ↓
Kubernetes performs rollout
             ↓
New pods start
             ↓
Live portfolio is updated
```

No manual Docker build or Kubernetes deployment is required after the code is committed.

---

# 10. Checking the Deployed Docker Image

To see which Docker image is currently running in AKS:

```bash
kubectl get deployment flask-portfolio -n flask-app -o jsonpath='{.spec.template.spec.containers[0].image}'
```

Example output:

```text
priyadocker2025/flask-portfolio:18
```

This confirms which image version is currently deployed.

Previously, for example, the application was running:

```text
priyadocker2025/flask-portfolio:8
```

After later pipeline runs, a newer build deployed:

```text
priyadocker2025/flask-portfolio:18
```

Build numbers do not need to be consecutive successful deployments because Azure DevOps can allocate Build IDs to other pipeline runs, including testing or failed runs.

---

# 11. Starting the AKS Cluster

The AKS cluster can be stopped when it is not required and started again later.

Start the cluster:

```bash
az aks start \
  --name flask-aks-cluster \
  --resource-group rg-flask-aks
```

Check the status:

```bash
az aks show \
  --name flask-aks-cluster \
  --resource-group rg-flask-aks \
  --query powerState.code \
  -o tsv
```

Expected output:

```text
Running
```

---

# 12. Connecting kubectl to AKS

After opening a new Azure Cloud Shell session, retrieve the AKS credentials:

```bash
az aks get-credentials \
  --resource-group rg-flask-aks \
  --name flask-aks-cluster \
  --overwrite-existing
```

This updates the Kubernetes configuration so that `kubectl` knows which AKS cluster to communicate with.

Then check the pods:

```bash
kubectl get pods -n flask-app
```

---

# 13. Getting the Application IP Address

Run:

```bash
kubectl get service -n flask-app
```

Find:

```text
flask-portfolio-service
```

and look at its:

```text
EXTERNAL-IP
```

The external IP is the public entry point to the Flask application.

---

# 14. Useful Kubernetes Commands

Check pods:

```bash
kubectl get pods -n flask-app
```

Check services:

```bash
kubectl get service -n flask-app
```

Check deployments:

```bash
kubectl get deployments -n flask-app
```

Check the deployed Docker image:

```bash
kubectl get deployment flask-portfolio -n flask-app -o jsonpath='{.spec.template.spec.containers[0].image}'
```

Inspect a pod when troubleshooting:

```bash
kubectl describe pod <pod-name> -n flask-app
```

Check deployment rollout:

```bash
kubectl rollout status deployment/flask-portfolio -n flask-app
```

---

# 15. Stopping AKS

To reduce unnecessary Azure usage when the cluster is not required:

```bash
az aks stop \
  --name flask-aks-cluster \
  --resource-group rg-flask-aks
```

Check the status:

```bash
az aks show \
  --name flask-aks-cluster \
  --resource-group rg-flask-aks \
  --query powerState.code \
  -o tsv
```

Expected output:

```text
Stopped
```

The cluster can later be started again using `az aks start`.

---

# 16. CI/CD Demo Procedure

For a live demonstration:

### Step 1 – Start AKS

```bash
az aks start \
  --name flask-aks-cluster \
  --resource-group rg-flask-aks
```

### Step 2 – Connect kubectl

```bash
az aks get-credentials \
  --resource-group rg-flask-aks \
  --name flask-aks-cluster \
  --overwrite-existing
```

### Step 3 – Verify pods

```bash
kubectl get pods -n flask-app
```

All Flask and MySQL pods should show:

```text
Running
```

### Step 4 – Get the application IP

```bash
kubectl get service -n flask-app
```

Open the LoadBalancer external IP in a browser.

### Step 5 – Make a code change

Open:

```text
templates/portfolio.html
```

Make a small visible change to the portfolio.

### Step 6 – Commit the change

Commit the change to:

```text
main
```

Do not manually run the pipeline.

The commit automatically triggers the CI/CD pipeline.

### Step 7 – Watch Azure DevOps

Open:

```text
Pipelines → flask-portfolio
```

Observe:

```text
Build and Push
      ↓
Deploy to AKS
```

Both stages should complete successfully.

### Step 8 – Verify the new image

```bash
kubectl get deployment flask-portfolio -n flask-app -o jsonpath='{.spec.template.spec.containers[0].image}'
```

The command should show the newly deployed Docker image tag.

### Step 9 – Verify the live application

Return to the portfolio in the browser and refresh the page.

The new code change should now be visible.

This demonstrates the complete CI/CD process:

```text
Code → Commit → Build → Docker Hub → Deploy → AKS → Live Application
```

---

# 17. Troubleshooting

## ImagePullBackOff

If a Flask pod shows:

```text
ImagePullBackOff
```

inspect it:

```bash
kubectl describe pod <pod-name> -n flask-app
```

One possible cause is that AKS cannot authenticate with the private Docker Hub repository.

Verify that `dockerhub-secret` exists and that `deployment.yaml` contains:

```yaml
imagePullSecrets:
  - name: dockerhub-secret
```

## kubectl asks for credentials

If this appears:

```text
You must be logged in to the server
```

run:

```bash
az aks get-credentials \
  --resource-group rg-flask-aks \
  --name flask-aks-cluster \
  --overwrite-existing
```

Then retry the `kubectl` command.

---

# What I Learned

Through this project I practiced:

- Containerizing a Flask application with Docker
- Using Docker Hub as a private container registry
- Deploying containerized applications to Kubernetes
- Working with Azure Kubernetes Service
- Creating Kubernetes deployments and services
- Managing Kubernetes secrets
- Building an automated Azure DevOps CI/CD pipeline
- Automatically building and tagging Docker images
- Automatically deploying new application versions to AKS
- Troubleshooting Kubernetes `ImagePullBackOff` errors
- Verifying deployments using Kubernetes commands

The main benefit of the CI/CD pipeline is automation. A developer only needs to commit a code change, and the pipeline handles the build, container image creation, image push, and deployment to Kubernetes in a repeatable and consistent way.
