// Se connecter à la base admin pour créer l'utilisateur
db = db.getSiblingDB('admin');

// Créer l'utilisateur spécifique pour l'application
db.createUser({
    user: 'todo_user',
    pwd: 'passer',
    roles: [
        {
            role: 'readWrite',
            db: 'todo_db'
        },
        {
            role: 'dbAdmin',
            db: 'todo_db'
        }
    ]
});


// Se connecter à la base todo_db
db = db.getSiblingDB('todo_db');

// Création des collections
db.createCollection('todo');

// Création des index
db.todo.createIndex({ "name": "text", "desc": "text" });
db.todo.createIndex({ "date": 1 });