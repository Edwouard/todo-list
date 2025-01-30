# 📝 Application de Gestion de Tâches (ToDo List)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.6-green)](https://www.mongodb.com/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-lightgrey)](https://flask.palletsprojects.com/)

Une application web de gestion de tâches, construite avec Flask et MongoDB, déployable via Docker et Kubernetes.

## ✨ Fonctionnalités

- 📋 Gestion des tâches (CRUD)
- 🔍 Recherche avancée avec filtres multiples
- 🏷️ Système de priorités
- 📅 Organisation par dates
- 🔄 Suivi du statut des tâches
- 🎨 Interface utilisateur intuitive


## 🚀 Installation

### Prérequis

- Python 3.8+
- MongoDB 4.6+
- Docker & Docker Compose (optionnel)
- kubectl & minikube (pour déploiement Kubernetes)

### Installation Locale

```bash
# Cloner le dépôt
git clone https://github.com/Edwouard/todo-list.git
cd todo-list

# Configuration de l'environnement
chmod +x setup_local.sh
./setup_local.sh

# Démarrer l'application
flask run
```

### Utilisation avec Docker

```bash
# Construire et démarrer les conteneurs
docker-compose up -d

# Vérifier les logs
docker-compose logs -f
```

## 🛠️ Architecture du Projet

```
todo-list/
├── app/                    # Application Flask
│   ├── static/            # Ressources statiques
│   ├── templates/         # Templates HTML
│   ├── database.py        # Couche d'accès aux données
│   └── routes.py          # Routes de l'application
├── docker/                # Configuration Docker
├── scripts/              # Scripts utilitaires
└── docs/                 # Documentation
```

## 📚 Documentation Développeur

### Structure de la Base de Données

Les tâches sont stockées dans MongoDB avec la structure suivante :

```javascript
{
  "_id": ObjectId,
  "name": String,        // Nom de la tâche
  "desc": String,        // Description
  "date": Date,         // Date d'échéance
  "pr": String,         // Priorité (low/medium/high)
  "done": String        // Statut (yes/no)
}
```

### API Routes

- `GET /list` - Liste toutes les tâches
- `GET /completed` - Tâches terminées
- `GET /uncompleted` - Tâches en cours
- `POST /action` - Créer une tâche
- `GET /search` - Rechercher des tâches

## 🔧 Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet :

```env
FLASK_APP=app
FLASK_ENV=development
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=todo_user
MONGO_PASSWORD=your_password
```

## 🚢 Déploiement

### Avec Docker

```bash
# Construction de l'image
docker build -t todo-app .

# Déploiement
docker-compose up -d
```

### Avec Kubernetes

```bash
# Déploiement sur minikube
kubectl apply -f deployment.yaml
```

## 🤝 Contribution

1. Forkez le projet
2. Créez votre branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -am 'Ajout de fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request


## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.


## 🙏 Remerciements
- Tous les contributeurs qui ont participé au projet