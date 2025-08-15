pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nombre-usuario/order_api:latest"
        SLACK_WEBHOOK_URL = credentials('slack-webhook-url')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }
        stage('Push Docker Image') {
            steps {
                // Si tienes Docker Hub u otro registry configurado, descomenta la siguiente línea y configura credenciales
                // sh "docker push ${DOCKER_IMAGE}"
            }
        }
        stage('Notify Slack') {
            steps {
                sh """
                curl -X POST -H 'Content-type: application/json' --data '{"text": "La imagen Docker para *order_api* ha sido actualizada correctamente."}' $SLACK_WEBHOOK_URL
                """
            }
        }
    }
    post {
        failure {
            steps {
                sh """
                curl -X POST -H 'Content-type: application/json' --data '{"text": "El pipeline de *order_api* ha fallado. Revisa Jenkins."}' $SLACK_WEBHOOK_URL
                """
            }
        }
    }
}