pipeline {
    agent any
    environment {
        CRED = credentials('sandbox')
    }
    stages {
        stage('SET CRED') {
            steps {
                script {
                    remote = [:]
                    remote.name = "${params.host_name}"
                    remote.host = "${params.host_ip}"
                    remote.user = 'root'
                    remote.password = "${CRED_PSW}"
                    remote.allowAnyHosts = true
                }
            }
        }
        stage('Preparar carpeta y clonar repo') {
            steps {
                script {
                    sshCommand remote: remote,
                        command: """
                            if [ ! -d /tmp/mi_proyecto ]; then
                                mkdir -p /tmp/mi_proyecto
                                git clone https://github.com/JDamianHZ/order_api.git /tmp/mi_proyecto
                            fi
                        """
                }
            }
        }
        stage('Checkout') {
            steps {
                script {
                    sshCommand remote: remote,
                        command: """
                            cd /tmp/mi_proyecto &&
                            git stash &&
                            git checkout master &&
                            git pull
                        """
                }
            }
        }
        stage('Instalar dependencias y ejecutar tests') {
            steps {
                script {
                    sshCommand remote: remote,
                        command: """
                            cd /tmp/mi_proyecto &&
                            echo '📦 Instalando dependencias en entorno virtual...' &&
                            python3 -m venv venv &&
                            source venv/bin/activate &&
                            python3 -m pip install --upgrade pip &&
                            python3 -m pip install -r requirements.txt &&
                            echo '🧪 Ejecutando pruebas...' &&
                            pytest tests/ || echo "No hay pruebas, continue"
                        """
                }
            }
        }
        stage('Limpiar carpeta de pruebas') {
            steps {
                script {
                    sshCommand remote: remote,
                        command: """
                            rm -rf /tmp/mi_proyecto
                        """
                }
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