import requests
from bs4 import BeautifulSoup


url='http://books.toscrape.com/catalogue/libertarianism-for-beginners_982/index.html'
reponse=requests.get(url)
if reponse.ok :
    soup = BeautifulSoup(reponse.text, 'html.parser')
    tabSoup=soup.find("table", {"class": "table table-striped"})  #je récupère le tableau d'inforamtion du produit
    list=tabSoup.findAll('td') #liste contenant les cellules du tableau
    UPC=list[0].text
    price_exc=list[2].text.replace('Â','')
    price_inc=list[3].text.replace('Â','')
    dispo=list[5].text
    reviews=list[6].text

    menuSoup=soup.find('ul', {"class": 'breadcrumb'}) #je récupère le sommaire pour la catégorie et le titre
    categ=menuSoup.findAll('a')[-1].text
    titre=menuSoup.find('li', {"class": "active"}).text

    Description=soup.findAll('p')[3].text #Ici la description ne se trouve dans aucune division interessante, pas encore trouvé de meilleurs moyen que de récuperer tous les paragraphes...

    image=soup.find('div', {'class':'item active'}).find('img')['src']#Je récupère l'url de l'image (incomplet)
    image=image.replace('../..', 'http://books.toscrape.com')# Et je le complète


    with open('fichier.csv','w') as file :
        file.write('title, product_page_url, universal_ product_code (upc),price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n')
        file.write(titre + ',' + url + ',' + UPC + ',' + price_inc + ',' + price_exc + ',' + dispo + ',' + Description + ',' + categ + ',' + reviews + ',' + image)

else:
    print(reponse)