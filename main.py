from bs4 import BeautifulSoup
from fonctions import *
import requests
import shutil
import time
import csv
import os

t=time.time()
dictionnaire_cat=dico_url_cat()
os.makedirs('fichierCsv',exist_ok=True)
os.makedirs('images',exist_ok=True)
for categ, valeur in dictionnaire_cat.items():
    os.makedirs('images/'+categ, exist_ok=True)
    dico_lien_livre=dico_url_livre(valeur)
    with open('fichierCsv/'+categ+'.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['title'] + ['product_page_url'] + ['universal_ product_code (upc)'] + ['price_including_tax'] +
            ['price_excluding_tax'] + ['number_available'] + ['product_description'] + ['category'] +
            ['review_rating'] + ['image_url']
        )
        for lien, valeurs in dico_lien_livre.items() :
            reponse=requests.get(lien)
            if reponse.ok :
                soup = BeautifulSoup(reponse.text, 'html.parser')
                tabSoup=soup.find("table", {"class": "table table-striped"})  #je récupère le tableau d'inforamtion du produit
                liste_tab=tabSoup.findAll('td') #liste contenant les cellules du tableau
                UPC=liste_tab[0].text
                price_exc=liste_tab[2].text.replace('Â','')
                price_inc=liste_tab[3].text.replace('Â','')
                dispo=liste_tab[5].text
                reviews=liste_tab[6].text

                titre=valeurs[0]

                Description = soup.find('meta', {'name':'description'})['content'].strip() #On récupère la description sans les saut de ligne

                image=valeurs[1]
                writer.writerow(
                    [titre] + [lien] + [UPC] + [price_inc] + [price_exc] + [dispo] + [Description] + [categ] +
                    [reviews] + [image])

                r = requests.get(image, stream=True)
                if r.ok :
                    titre=titre.replace('/','')
                    with open('images/'+categ+'/'+titre+'.jpeg', 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else :
                    print(r)
            else:
                print(reponse)
print(time.time()-t)