import requests
from bs4 import BeautifulSoup



def liste_url_livre(url) :
    liste_url=[]
    reponse=requests.get(url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    nb_url=soup.find('form',{'class':'form-horizontal'}).find('strong').text #Nombre de liens à récupérer dans la catégorie
    nb_url=int(nb_url)


    list_temp=soup.find("ol",{'class':'row'}).findAll('a') #On récupère les lien en double

    for i in range(len(list_temp)) : #On complète les liens
        list_temp[i]=list_temp[i]['href'].replace('../../..','https://books.toscrape.com/catalogue')
    list_temp = list(set(list_temp)) #On supprime les doublons
    liste_url.extend(list_temp)




    if nb_url>20 : #si il y a plus d'une page
        url=url.replace('index.html','')
        nb_page=int(nb_url/20)
        for page in range(nb_page) :
            url2=url + 'page-' + str(page+2) +'.html'
            reponse = requests.get(url2)
            soup = BeautifulSoup(reponse.text, 'html.parser')
            list_temp=soup.find("ol",{'class':'row'}).findAll('a')

            for i in range(len(list_temp)):
                list_temp[i] = list_temp[i]['href'].replace('../../..', 'https://books.toscrape.com/catalogue')
            list_temp = list(set(list_temp))
            liste_url.extend(list_temp)

    return liste_url