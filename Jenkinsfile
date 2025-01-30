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
                    
                    # Attendre que MongoDB soit prêt
                    echo "=== Test de connexion MongoDB ==="
                    docker-compose -p todo-app exec -T mongodb mongosh --eval "db.runCommand('ping').ok"
                    
                    echo "=== Attente du démarrage des services ==="
                    sleep 15
                    
                    # Obtenir l'adresse IP du conteneur web
                    WEB_CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' todo-app-web-1)
                    echo "IP du conteneur web : $WEB_CONTAINER_IP"
                    
                    echo "=== Test de santé détaillé ==="
                    for i in $(seq 1 60); do
                        echo "Tentative $i/60"
                        RESPONSE=$(curl -s "http://${WEB_CONTAINER_IP}:5000/health")
                        STATUS=$?
                        
                        echo "Code retour curl : $STATUS"
                        echo "Réponse brute :"
                        echo "$RESPONSE"
                        
                        if [ $STATUS -eq 0 ] && echo "$RESPONSE" | grep -q '"status":"healthy"'; then
                            echo "✅ Application en bonne santé!"
                            exit 0
                        fi
                        
                        if [ $((i % 10)) -eq 0 ]; then
                            echo "=== État des conteneurs ==="
                            docker-compose -p todo-app ps
                            echo "=== Derniers logs de l'application ==="
                            docker-compose -p todo-app logs --tail=20 web
                        fi
                        
                        sleep 1
                    done
                    
                    echo "❌ Échec du démarrage"
                    echo "=== Logs complets ==="
                    docker-compose -p todo-app logs
                    
                    exit 1
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