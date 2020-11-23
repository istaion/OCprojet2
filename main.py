import requests
from bs4 import BeautifulSoup
from fonctions import liste_url_livre


url='https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html'

liste_lien_livre=liste_url_livre(url)
with open('fichier.csv', 'w') as file:
    file.write( 'title; product_page_url; universal_ product_code (upc); price_including_tax; price_excluding_tax; number_available; product_description; category; review_rating;image_url\n')
    for lien in liste_lien_livre :
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

            menuSoup=soup.find('ul', {"class": 'breadcrumb'}) #je récupère le sommaire pour la catégorie et le titre
            categ=menuSoup.findAll('a')[-1].text
            titre=menuSoup.find('li', {"class": "active"}).text

            Description = soup.find('meta', {'name':'description'})['content'].replace(';',',').strip() #On récupère la description sans les points virgules et les saut de ligne pour le csv

            image=soup.find('div', {'class':'item active'}).find('img')['src']#Je récupère l'url de l'image (incomplet)
            image=image.replace('../..', 'http://books.toscrape.com')# Et je le complète


            file.write(titre + ' ; ' + url + ' ; ' + UPC + ' ; ' + price_inc + ' ; ' + price_exc + ' ; ' + dispo + ' ; ' + Description + ' ; ' + categ + ' ; ' + reviews + ' ; ' + image + '\n')

        else:
            print(reponse)