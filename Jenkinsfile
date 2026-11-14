pipeline {
    agent any
    environment {
        // Replace with your Docker Hub username.
        IMAGE_NAME = 'YOUR_DOCKERHUB_USERNAME/employee-attendance'
        K8S_NAMESPACE = 'attendance'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Validate Python') {
            steps { sh 'python3 -m py_compile app.py' }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER -t $IMAGE_NAME:latest .'
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push "$IMAGE_NAME:$BUILD_NUMBER"
                        docker push "$IMAGE_NAME:latest"
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                // Configure kubectl access on the Jenkins agent before running this stage.
                sh '''
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/configmap.yaml
                    kubectl apply -f k8s/secret.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl set image deployment/attendance-web attendance="$IMAGE_NAME:$BUILD_NUMBER" -n "$K8S_NAMESPACE"
                    kubectl rollout status deployment/attendance-web -n "$K8S_NAMESPACE" --timeout=180s
                '''
            }
        }
    }
    post {
        success { echo 'Build, image push and Kubernetes deployment completed.' }
        failure { echo 'Pipeline failed. Check Console Output.' }
    }
}
