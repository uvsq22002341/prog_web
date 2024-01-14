## Étapes pour débuter

- Mettre en place les clés SSH (voir TD 0)
- Créer un projet vide sur `etulab.univ-amu.fr` sans README.md
- `git clone git@etulab.univ-amu.fr:[....]/[....].git` pour cloner votre projet 
- `cd [....]` de façon à aller dans votre projet
- `git pull git@etulab.univ-amu.fr:estellon/webrt_project_start_2023_2024.git` pour récupérer les *commits* du projet "webrt_project_start"
- `git push` pour envoyer les modifications vers le dépôt distant
- `python -m virtualenv venv` (ou `python3` si vous êtes sous Linux) pour créer l'environnement virtuel
- `code .` pour ouvrir le dossier `.` dans Visual Studio Code 
- Dans un terminal de Visual Studio Code (avec `(venv)` au début du prompt):
    - `pip install -r requirements.txt`
    - `python init_db.py`
    - `pytest -v`
    - `flask run`
- Ouvrir [`http://localhost:5000`](http://localhost:5000) dans un navigateur
- Essayer de se connecter avec `user@example.com` et le mot de passe `secret`