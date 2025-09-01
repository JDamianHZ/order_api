pipeline {
    agent any

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
                echo '📦 Instalando dependencias...'
                sh 'pip install -r requirements.txt'  // Ejemplo Python
            }
        }

        stage('Pruebas') {
            steps {
                echo '🧪 Ejecutando pruebas...'
                sh 'pytest tests/'  // Ajusta a tu framework
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
