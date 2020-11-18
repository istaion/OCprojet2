import requests
from bs4 import BeautifulSoup


url='http://books.toscrape.com/catalogue/libertarianism-for-beginners_982/index.html'
reponse=requests.get(url)
if reponse.ok :
    soup = BeautifulSoup(reponse.text, 'html.parser')
    tabSoup=soup.find("table", {"class": "table table-striped"})
    list=tabSoup.findAll('td')
    UPC=list[0].text
    price_exc=list[2].text.replace('Â','')
    price_inc=list[3].text.replace('Â','')
    dispo=list[5].text
    reviews=list[6].text

    menuSoup=soup.find('ul', {"class": 'breadcrumb'})
    categ=menuSoup.findAll('a')[-1].text
    titre=menuSoup.find('li', {"class": "active"}).text

    Description=soup.findAll('p')[3].text
    image=soup.find('div', {'class':'item active'}).find('img')['src']
    image=image.replace('../..', 'http://books.toscrape.com')


    with open('fichier.csv','w') as file :
        file.write('title, product_page_url, universal_ product_code (upc),price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n')
        file.write(titre + ',' + url + ',' + UPC + ',' + price_inc + ',' + price_exc + ',' + dispo + ',' + Description + ',' + categ + ',' + reviews + ',' + image)