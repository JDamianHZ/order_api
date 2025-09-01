pipeline {
    agent any  // Correrá en el nodo que Jenkins tenga disponible

    environment {
        APP_ENV = 'production'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Instalar dependencias') {
            steps {
                echo '📦 Instalando dependencias en contenedor Docker...'
                sh '''
                    docker run --rm -v $PWD:/app -w /app python:3.11 \
                    /bin/bash -c "pip install --upgrade pip && pip install -r requirements.txt"
                '''
            }
        }

        stage('Pruebas') {
            steps {
                echo '🧪 Ejecutando pruebas en contenedor Docker...'
                sh '''
                    docker run --rm -v $PWD:/app -w /app python:3.11 \
                    /bin/bash -c "pytest tests/"
                '''
            }
        }

        stage('Deploy a producción') {
            when {
                branch 'master'
            }
            steps {
                echo '🚀 Haciendo deploy a producción...'
                // sh './scripts/deploy.sh'  <- aquí tu despliegue real
            }
        }
    }

    post {
        success {
            echo '✅ Build exitoso'
        }
        failure {
            echo '❌ Falló el pipeline'
            error("El build falló, no se permitirá merge a master")
        }
    }
}
