def remote = [:]

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
                    remote.name = "${params.host_name}"
                    remote.host = "${params.host_ip}"
                    remote.user = 'root'
                    remote.password = "${CRED_PSW}"
                    remote.allowAnyHosts = true
                    echo "🔑 Credenciales configuradas para ${remote.user}@${remote.host}"
                }
            }
        }

        stage('Checkout') {
            steps {
                sshCommand remote: remote,
                    command: """
                        cd /root/mi_proyecto &&
                        git stash &&
                        git checkout master &&
                        git pull
                    """
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
                sshCommand remote: remote,
                    command: "./scripts/deploy.sh"
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
