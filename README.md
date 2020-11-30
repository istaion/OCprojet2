# OCprojet2
Le programme recupère les informations sur les livres de booktoscrap.com et les enregistre dans des fichiers csv par catégorie. Il télecharge également les images des couvertures.

## utilisation

Dans votre terminal placez vous à la racine du projet puis :

### Créer votre environnement virtuel :


```bash
python3 -m venv env
```

### Activer votre environnement :

linux ou mac :
```bash
source env/bin/activate
```

windows :

```bash
env\\Scripts\\activate.bat
```

### Installer les packages :

```bash
pip install -r requierements.txt
```

### Executer le programme :

```bash
python3 main.py
```

## Fonctionnement

Les csv contenant les informations des livres d'une catégorie sont enregistrés dans un dossier fichierCsv. 

Les images sont enregistrées dans des dossiers correspondants aux catégories des livres à l'interieur d'un dossier images. 

Pour ouvrir les csv utiliser la virgule (,) comme séparateur et le double guillemet (") comme séparateur de chaine de caractère.

Le programme met environ 15 minutes à s'executer complétement.
