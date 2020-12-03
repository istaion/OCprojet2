from bs4 import BeautifulSoup
from fonctions import *
import requests
import shutil
from slugify import slugify
import csv
import os

dictionnaire_cat = dico_url_cat()  # Dictionnaire avec en clés le nom des catégories et les liens en valeurs

os.makedirs('fichierCsv', exist_ok=True)  # Création des dossiers qui vont contenir nos informations
os.makedirs('images', exist_ok=True)

for categ, valeur in dictionnaire_cat.items():
    os.makedirs('images/'+categ, exist_ok=True)  # Création d'un dossier par catégorie pour les images
    dico_lien_livre = dico_url_livre(valeur)    # Dictionnaire avec en clés les liens vers les pages des livres et en valeurs le titre et l'url de l'image
    with open('fichierCsv/'+categ+'.csv', 'w', encoding="utf-8") as file:
        writer = csv.writer(file)  # Initialisation de notre fichier csv
        writer.writerow(
            ['title'] + ['product_page_url'] + ['universal_ product_code (upc)'] + ['price_including_tax'] +
            ['price_excluding_tax'] + ['number_available'] + ['product_description'] + ['category'] +
            ['review_rating'] + ['image_url']
        )
        for lien, valeurs in dico_lien_livre.items():
            reponse = requests.get(lien)
            if reponse.ok:
                soup = BeautifulSoup(reponse.text, 'html.parser')
                tabSoup = soup.find("table", {"class": "table table-striped"})  # on récupère le tableau d'information du produit
                liste_tab = tabSoup.findAll('td')  # liste contenant les cellules du tableau
                UPC = liste_tab[0].text  # numéro UPC
                price_exc = liste_tab[2].text.replace('Â', '')  # prix hors taxe
                price_inc = liste_tab[3].text.replace('Â', '')  # prix avec taxe
                dispo = liste_tab[5].text  # nombre de livres disponibles
                reviews = liste_tab[6].text  # nombre de reviews

                titre = valeurs[0]  # titre du livre
                image = valeurs[1]  # url de l'image de couverture

                Description = soup.find('meta', {'name': 'description'})['content'].strip()  # On récupère la description sans les sauts de ligne

                writer.writerow(
                    [titre] + [lien] + [UPC] + [price_inc] + [price_exc] + [dispo] + [Description] + [categ] +
                    [reviews] + [image])  # On comlète le csv

                r = requests.get(image, stream=True)  # On télecharge les images
                if r.ok:
                    titre = slugify(titre)
                    with open('images/'+categ+'/'+titre+'.jpeg', 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else:
                    print(r)
            else:
                print(reponse)
        print('Les données de la catégorie ' + categ + ' ont été récupérées')
