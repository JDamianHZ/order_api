def remote = [:]
remote.name = "${params.host_name}"
remote.host = "${params.host_ip}"

pipeline {
    agent any

    environment {
        CRED = credentials('sandbox')  // credencial de SSH
        APP_ENV = 'production'
    }

    stages {
        stage('SET CRED') {
            steps {
                script {
                    remote.user = 'root'
                    remote.password = "${CRED_PSW}"
                    remote.allowAnyHosts = true
                    echo "🔑 Credenciales configuradas para ${remote.user}@${remote.host}"
                }
            }
        }

        stage('Checkout') {
            steps {
                echo "📂 Checkout simulado: git stash, checkout master y pull en /root/mi_proyecto"
            }
        }

        stage('Instalar dependencias y ejecutar tests') {
            steps {
                sshCommand remote: remote,
                    command: """
                        cd /root/mi_proyecto &&
                        echo '📦 Instalando dependencias...' &&
                        python3 -m pip install --upgrade pip &&
                        python3 -m pip install -r requirements.txt &&
                        echo '🧪 Ejecutando pruebas...' &&
                        pytest tests/
                    """
            }
        }

        stage('Deploy a producción') {
            when {
                branch 'master'
            }
            steps {
                echo "🚀 Deploy simulado: ./scripts/deploy.sh"
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
