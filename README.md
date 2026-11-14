# TeamTrack – Employee Attendance DevOps + Kubernetes Project

Develop on Windows, push to GitHub, build/push the image with Jenkins, and deploy to Kubernetes on AWS EC2.

## Project files
- `app.py`: Flask application
- `templates/`, `static/`: website UI
- `Dockerfile`: container build instructions
- `Jenkinsfile`: checkout, validate, build, push and deploy pipeline
- `k8s/`: Namespace, ConfigMap, Secret, Deployment and Service manifests

## A. Windows: run the application
Install Python 3, Git, Docker Desktop and VS Code. In PowerShell, from this folder:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000. Health endpoint: http://127.0.0.1:5000/health

If activation is blocked, run this in the current PowerShell window:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## B. Windows: build and test Docker
Start Docker Desktop:
```powershell
docker build -t employee-attendance:local .
docker run --rm -p 5000:5000 employee-attendance:local
```
Open http://localhost:5000. Stop with Ctrl+C.

## C. Push source to GitHub
Create an empty GitHub repository, then:
```powershell
git init
git add .
git commit -m "Initial employee attendance application"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
If `origin` already exists, do not add it again; inspect with `git remote -v`.

## D. AWS lab architecture and cost
Recommended learning layout: one Ubuntu EC2 for Jenkins and a second Ubuntu EC2 for a small single-node K3s Kubernetes lab. For comfortable labs, target at least 2 vCPU and 4 GB RAM per server. A single EC2 is possible for a small experiment but may run short of memory. AWS charges apply while instances and storage are running; stop or terminate resources when not in use.

Do not expose SSH (22), Jenkins (8080), or Kubernetes API (6443) to the whole internet. Restrict access to your own IP and use SSH keys. Allow Jenkins-to-Kubernetes communication only through trusted private networking/security-group rules.

## E. Jenkins setup
1. Install Java, Jenkins and Docker on the Jenkins EC2.
2. Install Jenkins plugins: Pipeline, Git, Credentials Binding.
3. Add a Jenkins username/password credential with ID `dockerhub-creds`. Use a Docker Hub access token as the password.
4. Replace `YOUR_DOCKERHUB_USERNAME` in the `IMAGE_NAME` value in this Jenkinsfile.
5. Ensure the Jenkins agent can run Docker commands.
6. Configure `kubectl` on the Jenkins agent to securely access K3s.
7. Create a Pipeline job using Pipeline script from SCM, select Git, enter your GitHub repository URL, and set script path to `Jenkinsfile`.

The Deploy stage will fail until kubectl access is configured. Do not place a cluster-admin kubeconfig in an exposed or untrusted environment.

## F. Kubernetes verification
After K3s is installed and Jenkins has kubectl access:
```bash
kubectl get nodes
kubectl get all -n attendance
kubectl get pods -n attendance -o wide
kubectl get svc -n attendance
kubectl rollout status deployment/attendance-web -n attendance
```
The NodePort is 30080. For a temporary lab, restrict inbound access to your own IP; prefer Ingress or a load balancer for a public service.

## Practice commands
```bash
kubectl describe pod POD_NAME -n attendance
kubectl logs POD_NAME -n attendance
kubectl scale deployment attendance-web --replicas=4 -n attendance
kubectl rollout history deployment/attendance-web -n attendance
kubectl rollout undo deployment/attendance-web -n attendance
kubectl delete namespace attendance
```

## Important limitations
This is a learning demo. Employee records are in Python memory, so they reset when a Pod restarts and are not shared between replicas. The Deployment manifest starts with a placeholder Nginx image; Jenkins replaces it with the built Docker Hub image during deployment. Kubernetes Secret is not automatically encrypted in every cluster. Replace the demo secret and configure encryption/RBAC before production. Add a database, persistent storage, TLS, image scanning and proper secret management before production use.
