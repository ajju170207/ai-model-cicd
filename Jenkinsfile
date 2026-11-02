
pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
    PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    IMAGE_NAME = "ai-model:latest"
        }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup and Train AI Model') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/python train_model.py
                '''
            }
        }

        stage('Test AI Model') {
            steps {
                sh '''
                    PYTHONPATH=. .venv/bin/python -m pytest tests/ -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Test Docker Container') {
            steps {
                sh '''
                    docker rm -f ai-model-test || true

                    docker run -d \
                        --name ai-model-test \
                        -p 8001:8000 \
                        $IMAGE_NAME

                    for i in $(seq 1 30); do
                        if curl -fsS http://localhost:8001/health; then
                            echo "Docker application is healthy"
                            exit 0
                        fi
                        sleep 2
                    done

                    docker logs ai-model-test
                    exit 1
                '''
            }
        }

        stage('Load Image into Minikube') {
            steps {
                sh 'minikube image load $IMAGE_NAME'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/deployment.yaml

                    kubectl rollout restart deployment/ai-model-deployment

                    kubectl rollout status deployment/ai-model-deployment --timeout=180s
                '''
            }
        }

        stage('Verify Docker') {
    steps {
        sh 'whoami'
        sh 'echo $PATH'
        sh 'which docker'
        sh 'docker --version'
        sh "docker info --format '{{.ServerVersion}}'"
    }
}
    }

    post {
        always {
            sh 'docker rm -f ai-model-test || true'
        }

        success {
            echo 'CI/CD Pipeline Completed Successfully!'
        }

        failure {
            echo 'CI/CD Pipeline Failed. Check Console Output.'
        }
    }
}
