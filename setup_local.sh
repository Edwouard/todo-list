#!/bin/bash

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "Configuration de l'environnement de développement local"
echo "----------------------------------------------------"

# Vérification de Python
python3 --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Python3 n'est pas installé${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 est installé${NC}"

# Vérification de MongoDB
mongod --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ MongoDB n'est pas installé${NC}"
    echo "Veuillez installer MongoDB avant de continuer"
    exit 1
fi
echo -e "${GREEN}✓ MongoDB est installé${NC}"

# Création et activation de l'environnement virtuel
echo "Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

# Installation des dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Démarrage de MongoDB (si nécessaire)
if ! pgrep mongod >/dev/null; then
    echo "Démarrage de MongoDB..."
    sudo systemctl start mongodb
fi

# Création du fichier .env
echo "Configuration des variables d'environnement..."
cat > .env << EOL
FLASK_APP=app
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=todo_user
MONGO_PASSWORD=passer
MONGO_DB=todo_db
EOL

# Initialisation de la base de données
echo "Initialisation de la base de données..."
python scripts/init_db.py

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ Configuration terminée avec succès !${NC}"
    echo "Pour démarrer l'application :"
    echo "1. Activez l'environnement virtuel : source venv/bin/activate"
    echo "2. Lancez l'application : flask run"
else
    echo -e "\n${RED}❌ Une erreur est survenue lors de la configuration${NC}"
fi