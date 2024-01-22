
## GeoJSON
> Ressource: https://www.infobelpro.com/fr/blog/format-geojson

### Feature
> Chaque entité individuelle, qu'il s'agisse d'un parc urbain, d'une rivière sinueuse ou d'une montagne imposante, est encapsulée dans une entité (Feature), souvent désignée comme une entité délimitée dans l'espace.

```json
{
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [
            40.783360355115676,
            -73.96533474251368
        ]
    },
    "properties": {
        "name": "Central Park"
    }
}
```

En GeoJson et pour Mapbox, ça représente un ensemble qui contient:
- les propriétés, c'est à dire les données associées
- la géométrie (**geometry**) un sous-objet qui contient les données vectorielles permettant le rendu sur la carte, il y a plusieurs types (point, multiPoint, lineString, polygone...)

### Geometry
> Il s'agit du squelette de votre entité. Il représente la forme ou la structure physique réelle, qu'il s'agisse d'un point singulier, d'une séquence de points formant une ligne ou d'une série de points créant une forme fermée.

C'est un sous-objet d'une feature qui contient les **coordonnées**, sous forme de paire longitude/latitude, ou d'un tableau de paires pour les lineStrings.

## Sets
### Datasets
> A dataset is an editable collection of GeoJSON features. Datasets are distinct from tilesets in that datasets can be edited on a feature-by-feature basis, **but cannot be used directly in Mapbox Studio style.**

De ce que j'ai compris, permet l'édition *manuelle* des données mais doit être utilisé pour construire un **tileset**.

#### Formats acceptés pour l'upload :
> https://docs.mapbox.com/help/troubleshooting/uploads/#accepted-file-types-and-transfer-limits

CSV ou geoJson, mais les CSV doivent être formatés comme un geoJson si on veut afficher des lignes plutot que des points etc.

### Tilesets
> https://docs.mapbox.com/studio-manual/reference/tilesets/

> Tilesets are the primary data format for Mapbox maps. Whether you start with your own custom data or you create a dataset first, converting your data into a tileset will allow you to add it to a Mapbox map.

Le bloc de construction de base de Mapbox, qui permet l'affichage.
Ca consiste en une collection de données vectorielles (ou raster pour les images satellites) placées sur une grille avec 22 niveaux de zoom pré-définis. Ca permet d'afficher des choses différentes selon le niveau de zoom.

Si j'ai bien compris, les tilesets doivent être générés avec l'outil **Mapbox Tiling Service** puis chargés avec l'**Uploads API** ou bien créés manuellement sur la plateforme, soit depuis des données brutes soit depuis un **dataset**.

#### Format de données requis
> Your raw geographic source data must be formatted as line-delimited GeoJSON (uncompressed line-delimited sequences of GeoJSON features).

> https://docs.mapbox.com/mapbox-tiling-service/guides/tileset-sources/

Les tilesets nécessitent des données GeoJson, formatées non pas en **Feature Collection** (la façon classique de rassembler des features en GeoJson) mais avec un retour à la ligne entre chaque Feature.

Les propriétés des features **ne peuvent pas être listées sous forme d'objet ou de tableau** simplement séparées par des virgules. Le format est donc suffisament différent du véritable GeoJson pour être incompatible.

### Mapbox Tiling Service (MTS)
L'outil pour générer et mettre à jour les tilesets à partir de données brutes et de recettes (recipes).

#### Utiliser MTS
Pour utiliser MTS, on a le choix entre deux interfaces en ligne de commande, une en **Python** (Tilesets CLI) et une en **Node.js** (MTS Data Sync). On peut aussi utiliser l'API dédiée **MTS API**

Pour utiliser l'API, il faut préparer les données dans le format spécifique aux tilesets, ce qui veut dire soit repenser le générateur de GeoJson pour qu'il génére directement ce format ou fasse la conversion, soit utiliser directement **Tilesets CLI** ou **MTS Data Sync**, auquel cas on peux se passer de l'API.

D'après ce que je sais de ce genre de trucs, ça veux dire installer ces outils sur le serveur et déclencher des "jobs" dans le back.

Modifier le générateur de GeoJson pourrait rendre les fichiers moins exploitables pour Jérémie, qui peux convertir du "vrai" GeoJson mais probablement pas ce format spécifique à Mapbox.

J'en déduis que l'API n'est pertinente que dans un environnement ou il n'est pas possible d'utiliser les outils CLI, par exemple coté client, mais à vérifier.

#### Recipes
> https://docs.mapbox.com/mapbox-tiling-service/reference/

> A tileset recipe is a JSON document containing configuration options that tell Mapbox Tiling Service (MTS) how to turn tileset source data into vector tiles.

Pour générer un tileset, on utilise en plus des données une recette qui détaille explicitement toute la configuration: une seule layer ou multilayer, niveaux de zoom autorisés, affichage par niveau de zoom de feature spécifiques, manipulation des attributs, filtres, relations entre features...

C'est un peu cryptique encore pour moi mais à mon avis on peux s'en sortir avec une configuration basique sans rentrer dans les fonctionnalités avancées.

## APIs

### Tilequery API
> https://docs.mapbox.com/api/maps/tilequery/
C'est l'API qui sert à sélectionner et extraire des features d'un tileset pour en faire ce qu'on veut: récupérer seulement les données dans une certaine zone sur la carte, limiter le nombre de features affichées, filtrer les types de géometries affichées, afficher seulement les points contenu dans un polygone...

### Uploads API
> https://docs.mapbox.com/api/maps/uploads/


