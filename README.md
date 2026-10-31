# Online Bookstore — DevOps Case Study

A beginner-friendly Flask online bookstore used to demonstrate Git, Docker, Jenkins CI/CD, and Kubernetes deployment.

## Application features
- View a sample book catalogue.
- Add a book with title, author, price, and description.
- Health endpoint: `/health`.
- SQLite database is created automatically.

## 1. Run locally (Windows)
Open Command Prompt in this project folder:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000`.

## 2. Test
```bat
py -m pytest -q
```

## 3. Build and run with Docker
Replace nothing for the local test image name:

```bat
docker build -t online-bookstore:latest .
docker run -d --name bookstore -p 5000:5000 online-bookstore:latest
```

Open `http://localhost:5000`. Check:
```bat
docker ps
docker logs bookstore
```
Stop/remove:
```bat
docker rm -f bookstore
```

## 4. Push source to GitHub
Create an empty GitHub repository, then run (replace the URL with your repository URL):

```bat
git init
git add .
git commit -m "Initial online bookstore project"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

## 5. Docker Hub preparation
1. Create a Docker Hub account and a repository named `online-bookstore`.
2. In `Jenkinsfile` and `k8s/deployment.yaml`, replace `YOUR_DOCKERHUB_USERNAME` with your Docker Hub username.
3. Do not put your Docker Hub password in any file or Git repository.

## 6. Jenkins setup (Windows)
Prerequisites: Jenkins, Git, Python, Docker Desktop, and kubectl installed and available to the Windows account running the Jenkins agent. Docker Desktop must be running. Enable Kubernetes in Docker Desktop if you plan to deploy to the local cluster.

1. Open Jenkins and install suggested plugins plus **Pipeline**, **Git**, and **Credentials Binding** if missing.
2. In **Manage Jenkins → Credentials → (global) → Add Credentials**, choose **Username with password**. Enter your Docker Hub username and a Docker Hub access token as the password. Set ID to `dockerhub-creds`.
3. Edit the `IMAGE_NAME` value in `Jenkinsfile` to `YOUR_DOCKERHUB_USERNAME/online-bookstore`.
4. Edit the image in `k8s/deployment.yaml` to the same Docker Hub image name.
5. Push the changes to GitHub.
6. Create **New Item → Pipeline**. Choose **Pipeline script from SCM**, SCM **Git**, enter your repository URL, branch `*/main`, and script path `Jenkinsfile`.
7. Save and click **Build Now**. Open **Console Output** to see each stage.

Important: this Jenkinsfile uses Windows `bat` commands. The Jenkins agent must run on Windows and have `python`, `docker`, and `kubectl` on its PATH. If Jenkins runs as a Windows service, it may not share your interactive user's Docker Desktop/Kubernetes access. If Docker or kubectl fails only in Jenkins, run the Jenkins agent under the same Windows account that has Docker Desktop and Kubernetes configured, or configure a dedicated Jenkins agent with those tools and permissions.

## 7. Kubernetes deployment
In Docker Desktop, open **Settings → Kubernetes → Enable Kubernetes**, apply changes, and wait until the cluster is running. In Command Prompt:

```bat
kubectl config use-context docker-desktop
kubectl get nodes
```

The Jenkins pipeline applies `k8s/deployment.yaml` and `k8s/service.yaml` after pushing the image. To deploy manually:

```bat
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods
kubectl get services
kubectl rollout status deployment/online-bookstore
```

Open `http://localhost:30080`.

Useful checks:
```bat
kubectl get deployments
kubectl describe deployment online-bookstore
kubectl logs deployment/online-bookstore
```

To remove the Kubernetes resources:
```bat
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
```

## Pipeline flow
GitHub source → Jenkins checkout → install dependencies → pytest → Docker build → Docker Hub push → Kubernetes apply → expose through NodePort 30080.

## Troubleshooting
- `docker is not recognized`: start Docker Desktop and add Docker CLI to PATH; reopen Command Prompt/Jenkins agent.
- Docker daemon connection error: Docker Desktop is not running or Jenkins cannot access its engine.
- `kubectl` connection refused: enable Kubernetes in Docker Desktop and confirm `kubectl get nodes` works in the same account as Jenkins.
- `ImagePullBackOff`: check the image name in the Deployment and confirm it exists in Docker Hub and is public, or configure an image pull secret for a private repository.
- Port 30080 unavailable: run `kubectl get svc` and confirm the Service is `NodePort` with nodePort `30080`.
- SQLite data in this demo is stored inside the container filesystem and may be lost when the pod is replaced. This is acceptable for a classroom demo; a production app should use persistent storage and stronger secret management.

## One-minute demonstration order
1. Show the bookstore in the browser and add a sample book.
2. Show the project files: `Dockerfile`, `Jenkinsfile`, `k8s/deployment.yaml`, and `k8s/service.yaml`.
3. Show the GitHub repository.
4. Show Jenkins pipeline stages and successful Console Output.
5. Show Docker image in Docker Desktop or Docker Hub.
6. Show `kubectl get pods` and `kubectl get services`.
7. Open `http://localhost:30080` and show the deployed bookstore.
