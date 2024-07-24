# Portail Ailerons

### Installation & Prérequis

Le projet utilise [Poetry](https://python-poetry.org/) pour la gestion des dépendances. Poetry est un outil moderne pour la gestion des packages et des environnements virtuels en Python.

#### Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- **Python 3.7+** : Assurez-vous d'avoir une version de Python supérieure ou égale à 3.7. Vous pouvez vérifier votre version de Python en exécutant la commande suivante :
  ```bash
  python --version
  ```

- **Poetry** : Si Poetry n'est pas déjà installé sur votre machine, vous pouvez l'installer en suivant les instructions sur [le site officiel de Poetry](https://python-poetry.org/docs/#installation).

#### Installation

1. **Cloner le dépôt**

   Clonez le dépôt du projet en utilisant la commande suivante :
   ```bash
   git clone <URL_DU_REPO>
   ```
   Remplacez `<URL_DU_REPO>` par l'URL réelle du dépôt Git.

2. **Installer les dépendances**

   Accédez au répertoire du projet cloné et installez les dépendances en utilisant Poetry :
   ```bash
   cd <NOM_DU_REPERTOIRE_DU_PROJET>
   poetry install
   ```
   Cette commande installera toutes les dépendances spécifiées dans le fichier `pyproject.toml`.

3. **Lancer Poetry et l'environnement virtuel**

   Activez l'environnement virtuel géré par Poetry avec la commande suivante :
   ```bash
   poetry shell
   ```
   Cette commande vous placera dans un environnement virtuel isolé où toutes les dépendances du projet sont disponibles.
### Structure du Projet

Voici l'arborescence du projet :

```
├── ailerons_tracker_backend
│   ├── blueprints
│   │   └── static
│   ├── clients
│   ├── csv_parser
│   ├── forms
│   ├── models
│   ├── templates
│   │   └── shared
│   │       └── inputs
│   └── utils
├── migrations
│   └── versions
└── tests
    └── resources
```

#### Description des Dossiers

- **ailerons_tracker_backend** : Dossier principal du projet contenant tout le code source de l'application.

- **blueprints** : Ce dossier contient les "modules" Flask. Chaque blueprint gère des vues spécifiques et peut être imbriqué pour structurer l'API de manière modulaire.
  - **static** : Dossier pour les fichiers statiques (CSS, JavaScript, images).

- **clients** : Gère les interactions avec les clients, comme les API externes.

- **forms** : Regroupe les formulaires Flask-WTF utilisés dans l'application.

- **models** : Contient les modèles SQLAlchemy qui définissent la structure de la base de données.

- **templates** : Contient les templates Jinja2 utilisés pour générer les pages HTML.
    - **shared** : Templates partagés entre différentes parties de l'application.
      - **inputs** : Inputs communs utilisés dans différents formulaires.

- **utils** : Contient des fonctions utilitaires et des helpers pour l'application.

- **migrations** : Contient les fichiers de migration de la base de données, gérés par Alembic.
  - **versions** : Sous-dossier pour les différentes versions de migration.

- **tests** : Dossier principal pour les tests unitaires et d'intégration.
  - **resources** : Contient les ressources utilisées dans les tests (fichiers de test).

### Configuration et Lancement de l'Application

La configuration de l'application et sa création se font dans le fichier `__init__.py` du module principal.

#### Fonction `create_app`

La fonction `create_app` est une factory qui crée une instance de l'application Flask.

L'application Flask est créée:

```python
Flask(__name__, instance_relative_config=True)`. 
```

Une configuration définie par un objet est chargée:

```python
app.config.from_mapping(
  SECRET_KEY=os.getenv("APP_SECRET_KEY"),
  # URI can be found in Supabase dashboard, pwd can be reset there as well
  SQLALCHEMY_DATABASE_URI=f"postgresql://"
  f"redacted:{os.getenv('DB_PWD')}"
  "redacted",
  SERVER_NAME='127.0.0.1:5000',
  APPLICATION_ROOT='/'
)
```

La base de données et les migrations sont initialisées:

```python
db.init_app(app)
migrate.init_app(app, db)
```

Un fichier de configuration de l'instance est chargé si il existe, sauf en mode test où une configuration spécifique peut être passée:

```python
if test_config is None:
  # load the instance config, if it exists, when not testing
  app.config.from_pyfile('config.py', silent=True)
else:
  # load the test config if passed in
  app.config.from_mapping(test_config)
```

Le répertoire de l'instance est créé si nécessaire:

```python
os.makedirs(app.instance_path)`.
```

La protection CSRF est activée pour les formulaires:

```python
CSRFProtect().init_app(app)
```

Les extensions Jinja Partials sont enregistrées:

```python
register_extensions(app)`
```

Le gestionnaire de connexion est initialisé avec `login_manager.init_app(app)` et les fonctions de gestion des utilisateurs et de redirection non autorisée sont définies:

```python
@login_manager.user_loader
def load_user(user):
    app.logger.info(f"Logged: {user}")
    return User()
                                                                                        
@login_manager.unauthorized_handler
def unauthorized_handler():
    form = LoginForm()
    htmx = HTMX(current_app)
                                                                                        
    if htmx:
        return make_response(
            render_partial("login/login_section.jinja", form=form),
            push_url=url_for("portal.login.show")), 302
                                                                                        
    return render_template("base_layout.jinja", view=url_for("portal.login.show")), 302                                                                                        
```

Le blueprint principal de l'application est enregistré et activé:

```python
app.register_blueprint(portal)`.
```

La configuration des routes est affichée dans la console:

```python
app.logger.info(app.url_map)
```

### Base de Données

La connexion avec la base de données est définie dans le module `db` avec la configuration par défaut. Cette connexion est initialisée dans le fichier `__init__.py` de l'application, comme vu précédemment. La base de données utilisée est une base PostgreSQL hébergée dans le cloud par Supabase.

#### Configuration de la Base de Données

-   **Mot de Passe** : Le mot de passe de la base de données doit être défini dans une variable d'environnement. Il peut être retrouvé depuis le dashboard Supabase.
-   **URI de Connexion** : L'URI de connexion à la base de données est configurée dans l'application en utilisant les informations fournies par Supabase.

#### Modèles ORM avec SQLAlchemy

Les modèles ORM SQLAlchemy définissent les colonnes des tables en mappant des attributs Python et leurs types correspondants aux types de la base de données PostgreSQL. Voici un exemple de modèle pour la table `Picture` :
```python
""" Picture model """
from sqlalchemy import ForeignKey, Identity, Text, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column as mc, relationship as rel
from ailerons_tracker_backend.db import db

# pylint: disable=locally-disabled, not-callable

class Picture(db.Model):
    """ Picture model """

    id: Mapped[int] = mc(
        postgresql.BIGINT, 
        Identity(start=1, always=True), 
        primary_key=True, 
        unique=True
    )

    created_at: Mapped[str] = mc(
        postgresql.TIMESTAMP(timezone=True), 
        default=func.now()
    )

    url: Mapped[str] = mc(Text)

    individual: Mapped['Individual'] = rel(
        back_populates='pictures'
    )

    individual_id: Mapped[int] = mc(
        postgresql.BIGINT, 
        ForeignKey('individual.id')
    )
 ```
 
 #### Explication du Modèle `Picture`

-   **id** : Clé primaire unique de type BIGINT. La colonne utilise une séquence automatique (Identity) pour générer des valeurs uniques.
-   **created_at** : Colonne de type TIMESTAMP avec fuseau horaire, définie avec la date et l'heure actuelles par défaut.
-   **url** : Colonne de type Text pour stocker l'URL de l'image.
-   **individual** : Relation ORM avec le modèle `Individual`, définie pour permettre l'association bidirectionnelle entre `Picture` et `Individual`.
-   **individual_id** : Clé étrangère pointant vers l'ID de la table `Individual`.

### Gestion des Migrations

Les migrations permettent de gérer les modifications du schéma de la base de données au fil du temps. Alembic est utilisé pour gérer ces migrations, assurant que la base de données reste synchronisée avec les modèles définis dans le code.

Initialiser Alembic:

    flask db init

Créer un nouveau fichier de migration avec un message descriptif:

    flask db migrate -m "description de la migration"

Appliquer les migrations et mettre à jour la base de données vers la dernière version:

    flask db upgrade

Revenir à une version précédente de la base de données:

    flask db downgrade

### Relations entre les Tables

Les relations bidirectionnelles entre les tables sont définies dans les deux modèles associés, mais seule la table "enfant" doit définir la clé étrangère.

**Accès aux Objets Associés**

Lorsque vous récupérez un objet parent via une requête, les objets enfants associés sont accessibles directement. Par exemple :

```python
individual = db.session.get_one(Individual, 1)
for picture in individual.pictures:
  print(picture.url)
```

Vous pouvez également créer et associer des objets enfants à un objet parent directement dans le code :

```python
individual = Individual()
individual.pictures.append(Picture(url="http://example.com/image.jpg"))
db.session.add(individual)
db.session.commit()
```

### Exécution des Requêtes

Vous pouvez exécuter des requêtes en utilisant SQL brut ou en générant des statements sans rédiger de SQL directement :

1. **Génération des Statements**

   Utilisez les helpers fournis par l'objet `db` pour générer des statements SQL de manière programmatique :

   ```python
   stmt = db.select(Individual).where(Individual.id == 1)
   ```

2. **Exécution**

  Utilisez la session de base de données pour exécuter le statement :

   ```python
   res = db.session.execute(stmt)
   individuals = res.scalars().all()
   ```

 Scalars retourne une liste de résultats correspondant au statement. Il est nécessaire de spécifier le format de la réponse attendue ainsi.
 
 On procède pareillement pour supprimer une entrée:

  ```python
  ind = db.session.get_one(ind, 1)
  db.session.delete(ind)
  db.session.commit()
  ```

3. **Avec pandas**

  Il est aussi possible d'insérer directement des _dataframes_ avec pandas si leur structure correspond à un modèle:
  
  ```python
    df = pd.read_csv(csv_file)
    df.to_sql(name='record', con=db.engine,
          if_exists='append', index=False)
  ```
   
