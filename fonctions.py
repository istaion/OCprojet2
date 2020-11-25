import requests
from bs4 import BeautifulSoup


def dico_url_cat(): #Fonction récuperant les liens (en valeur) et le nom des catégories (en clés) dans un dictionnaire
    dico_cat={}
    reponse=requests.get("https://books.toscrape.com/")
    if reponse.ok:
        soup=BeautifulSoup(reponse.text, 'html.parser')
        soup_col=soup.find('ul',{'class':'nav nav-list'}).find('ul').findAll('a')


        for cat in range(len(soup_col)) :
            dico_cat[soup_col[cat].text.strip()]='https://books.toscrape.com/'+soup_col[cat]['href']
    else:
        print(reponse)
    return dico_cat


def dico_url_livre(url) : #Fonction récupérant les liens des livres (en clefs) et les titre et lien d'image (en url)
    dico_livre={}
    reponse=requests.get(url)
    if reponse.ok :
        soup = BeautifulSoup(reponse.text, 'html.parser')

        nb_url=soup.find('form',{'class':'form-horizontal'}).find('strong').text #Nombre de liens à récupérer dans la catégorie
        nb_url=int(nb_url)


        list_temp_livre=soup.find("ol",{'class':'row'}).findAll('a') #On récupère deux paragraphe pour chaque livre, un contenant l'url et l'image, un autre contenant l'url et le titre
        for i in range(int(len(list_temp_livre)/2)) : #on rentre dans le dictionnaire les liens en clefs et les titres et image en valeur (sous forme de liste)
            titre=list_temp_livre[i*2+1]['title']
            lien=list_temp_livre[i*2]['href'].replace('../../..', 'https://books.toscrape.com/catalogue')
            image=list_temp_livre[i*2].find('img')['src'].replace('../../../..', 'https://books.toscrape.com')
            dico_livre[lien]=[titre,image]




        if nb_url>20 : #si il y a plus d'une page
            url=url.replace('index.html','')
            nb_page=int(nb_url/20)
            for page in range(nb_page) :
                url2=url + 'page-' + str(page+2) +'.html'
                reponse = requests.get(url2)
                if reponse.ok :
                    soup = BeautifulSoup(reponse.text, 'html.parser')
                    list_temp_livre=soup.find("ol",{'class':'row'}).findAll('a')

                    for i in range(int(len(list_temp_livre)/2)):  # on rentre dans le dictionnaire les liens en clefs et les titres et image en valeur (sous forme de liste)
                        titre = list_temp_livre[i*2+1]['title']
                        lien = list_temp_livre[i*2]['href'].replace('../../..', 'https://books.toscrape.com/catalogue')
                        image = list_temp_livre[i*2].find('img')['src'].replace('../../../..', 'https://books.toscrape.com')
                        dico_livre[lien] = [titre, image]
                else:
                    print(reponse)
    else :
        print(reponse)

    return dico_livre
