
pipeline {
    agent any

    environment {
        IMAGE_NAME = "ranjitha28/online-bookstore"
        IMAGE_TAG = "latest"
        PYTHON = "C:/Users/ranji/AppData/Local/Programs/Python/Python313/python.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"%PYTHON%" -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f k8s/deployment.yaml'
                bat 'kubectl apply -f k8s/service.yaml'
                bat 'kubectl rollout restart deployment/online-bookstore'
                bat 'kubectl rollout status deployment/online-bookstore --timeout=120s'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'kubectl get deployments'
                bat 'kubectl get pods -l app=online-bookstore'
                bat 'kubectl get services'
            }
        }
    }

    post {
        success {
            echo 'Online Bookstore CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Please check the Jenkins console output.'
        }

        always {
            echo 'Online Bookstore pipeline execution finished.'
        }
    }
}

