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
                sh '''
                    timeout=60
                    counter=0
                    until curl -s http://localhost:5000/health > /dev/null; do
                        counter=$((counter + 1))
                        if [ $counter -gt $timeout ]; then
                            echo "L'application n'a pas démarré après $timeout secondes"
                            exit 1
                        fi
                        echo "En attente du démarrage de l'application..."
                        sleep 1
                    done
                    echo "Application démarrée avec succès!"
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