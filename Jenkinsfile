pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "todo-flask-app"
        DOCKER_TAG = "latest"
        DOCKER_COMPOSE_PROJECT = "todo-app"
        VENV_PATH = "/opt/jenkins_venv"
    }

    stages {
        stage('Préparation') {
            steps {
                cleanWs()
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/feature/jenkins-setup']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Edwouard/todo-list.git',
                        credentialsId: 'github-credentials'
                    ]]
                ])
            }
        }

        stage('Vérification de sécurité') {
            steps {
                echo "Analyse de sécurité des dépendances..."
                // Utilisation explicite de bash et modification de l'activation de l'environnement virtuel
                sh '''#!/bin/bash
                    # Activation de l'environnement virtuel de manière compatible avec sh
                    . ${VENV_PATH}/bin/activate
                    safety check -r requirements.txt
                    deactivate
                '''
            }
        }

        stage('Construction Docker') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -f docker/Dockerfile ."
                    sh "docker image inspect ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage("Analyse de l'image Docker") {
            steps {
                script {
                    sh '''
                        if command -v trivy &> /dev/null; then
                            trivy image ${DOCKER_IMAGE}:${DOCKER_TAG}
                        else
                            echo "Trivy n'est pas installé, analyse ignorée"
                        fi
                    '''
                }
            }
        }

        stage('Déploiement Local') {
            steps {
                script {
                    sh "docker-compose -p ${DOCKER_COMPOSE_PROJECT} down || true"
                    sh "docker-compose -p ${DOCKER_COMPOSE_PROJECT} up -d"
                    sh "docker-compose -p ${DOCKER_COMPOSE_PROJECT} ps"
                }
            }
        }

        stage('Tests de santé') {
            steps {
                sh '''#!/bin/bash
                    echo "Vérification de la santé de l'application..."
                    
                    # Attendre que les conteneurs soient "healthy" selon Docker
                    echo "Attente du démarrage des conteneurs..."
                    sleep 30  # Délai initial pour laisser les conteneurs démarrer
                    
                    # Fonction de test de santé
                    check_health() {
                        RESPONSE=$(curl -s http://localhost:5000/health)
                        echo $RESPONSE | grep -q '"status":"healthy"'
                        return $?
                    }
                    
                    # Boucle de vérification avec timeout
                    TIMEOUT=90
                    COUNTER=0
                    until check_health; do
                        COUNTER=$((COUNTER + 1))
                        if [ $COUNTER -gt $TIMEOUT ]; then
                            echo "Timeout après $TIMEOUT secondes"
                            echo "État des conteneurs :"
                            docker-compose -p todo-app ps
                            echo "Logs de l'application :"
                            docker-compose -p todo-app logs web
                            exit 1
                        fi
                        echo "Tentative $COUNTER/$TIMEOUT..."
                        sleep 5
                    done
                    
                    echo "✅ Application opérationnelle !"
                    curl -s http://localhost:5000/health | python -m json.tool
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline exécuté avec succès!"
        }
        
        failure {
            echo "Échec du pipeline"
            sh "docker-compose -p ${DOCKER_COMPOSE_PROJECT} down || true"
        }
        
        always {
            cleanWs()
        }
    }
}