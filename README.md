# ailerons-tracker-backend


Cloner le repo

Créer un nouvel environnement virtuel: $ python -m venv .venv 

Créer le script qui permet de réactiver l'environnement à chaque utilisation: 
Windows: $ .\\.venv\Scripts\activate 
Mac & Linux: $ source .venv/bin/activate

Si l'environnement ne s'active pas tout seul au lancement du projet et que l'étape précédente a été suivie: $ activate

Installer les dépendences: $ pip install -r requirements.txt

Demander les variables d'environnement .env pour les accès Supabase et les placer à la racine

Démarrer le serveur depuis le dossier racine: $ flask run

Mettre à jour requirements.txt après l'installation d'une nouvelle dépendence: $ pip freeze > requirements.txt
