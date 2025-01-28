pipeline {
    agent any

    environment {
        // Définition des variables d'environnement
        DOCKER_IMAGE = "todo-flask-app"
        DOCKER_TAG = "latest"
        DOCKER_COMPOSE_PROJECT = "todo-app"
    }

    stages {
        stage('Préparation') {
            steps {
                // Nettoyage de l'espace de travail
                cleanWs()
                
                // Clonage du dépôt avec credentials
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Edwouard/todo-list-flask.git',
                        credentialsId: 'github-credentials'
                    ]]
                ])
            }
        }

        stage('Vérification de sécurité') {
            steps {
                echo "Analyse de sécurité des dépendances..."
                // Vérification des vulnérabilités dans requirements.txt
                sh '''
                    if command -v safety &> /dev/null; then
                        safety check -r requirements.txt
                    else
                        pip install safety
                        safety check -r requirements.txt
                    fi
                '''
            }
        }

        stage('Tests') {
            steps {
                echo "Exécution des tests..."
                // Installation des dépendances dans un environnement virtuel
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    python -m pytest tests/
                '''
            }
        }

        stage('Construction Docker') {
            steps {
                echo "Construction des images Docker..."
                script {
                    // Construction de l'image Docker
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    
                    // Vérification de la construction
                    sh "docker image inspect ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('Analyse de l\'image Docker') {
            steps {
                echo "Analyse de sécurité de l'image Docker..."
                // Analyse de sécurité de l'image avec Trivy
                sh '''
                    if command -v trivy &> /dev/null; then
                        trivy image ${DOCKER_IMAGE}:${DOCKER_TAG}
                    else
                        echo "Trivy n'est pas installé, skip de l'analyse"
                    fi
                '''
            }
        }

        stage('Déploiement Local') {
            steps {
                echo "Déploiement avec Docker Compose..."
                script {
                    // Arrêt des conteneurs existants
                    sh "docker-compose -p ${DOCKER_COMPOSE_PROJECT} down || true"
                    
                    // Démarrage des nouveaux conteneurs
                    sh "docker-compose -p ${DOCKER_COMPOSE_PROJECT} up -d"
                    
                    // Vérification du déploiement
                    sh "docker-compose -p ${DOCKER_COMPOSE_PROJECT} ps"
                }
            }
        }

        stage('Tests de santé') {
            steps {
                echo "Vérification de la santé de l'application..."
                // Attente que l'application soit prête
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
            // Nettoyage en cas d'échec
            sh "docker-compose -p ${DOCKER_COMPOSE_PROJECT} down || true"
        }
        
        always {
            // Nettoyage de l'espace de travail
            cleanWs()
        }
    }
}