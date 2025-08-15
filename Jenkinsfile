pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nombre-usuario/order_api:latest"
        SLACK_WEBHOOK_URL = credentials('slack-webhook-url') // Debe configurarse en Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Si tienes Docker Hub u otro registry configurado
                    // docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                    //     docker.image("${DOCKER_IMAGE}").push()
                    // }
                }
            }
        }
        stage('Notify Slack') {
            steps {
                script {
                    def message = "La imagen Docker para *order_api* ha sido actualizada correctamente."
                    sh """
                    curl -X POST -H 'Content-type: application/json' --data '{"text": "${message}"}' $SLACK_WEBHOOK_URL
                    """
                }
            }
        }
    }
    post {
        failure {
            script {
                def message = "El pipeline de *order_api* ha fallado. Revisa Jenkins."
                sh """
                curl -X POST -H 'Content-type: application/json' --data '{"text": "${message}"}' $SLACK_WEBHOOK_URL
                """
            }
        }
    }
}