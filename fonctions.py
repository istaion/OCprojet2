import requests
from bs4 import BeautifulSoup


def category_url_dictionary():
    """
    function to retrieve the links and name of the category
    :return: Dictionary with category name (keys) and link (value)
    """
    category_dictionary = {}
    response = requests.get('https://books.toscrape.com/')
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        summary_soup = soup.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('a')
        for cat in range(len(summary_soup)):
            category_dictionary[summary_soup[cat].text.strip()] = \
                'https://books.toscrape.com/'+summary_soup[cat]['href']
    else:
        print(response)
    return category_dictionary


def book_url_dictionary(url):
    """
    function to retrieve the product page link, book name and picture link
    :param url: category page link
    :return: Dictionary with book url (keys) title and picture link (value)
    """
    book_dictionary = {}
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        # number of links to retrieve
        n_url = soup.find('form', {'class': 'form-horizontal'}).find('strong').text
        n_url = int(n_url)
        # Recover two paragraphs for each book,
        # the first containing the link and the image,
        # the second containing the link and the title
        temporary_list = soup.find('ol', {'class': 'row'}).findAll('a')
        # We put the links in keys and the title and image in value (in a list)
        for i in range(int(len(temporary_list)/2)):
            title = temporary_list[i*2+1]['title']
            link = temporary_list[i*2]['href'].replace('../../..', 'https://books.toscrape.com/catalogue')
            image = temporary_list[i*2].find('img')['src'].replace('../../../..', 'https://books.toscrape.com')
            book_dictionary[link] = [title, image]
        if n_url > 20:  # if there is more than one page
            url = url.replace('index.html', '')
            n_page = int(n_url/20)  # number of page
            for page in range(n_page):
                url2 = url + 'page-' + str(page+2) + '.html'
                response = requests.get(url2)
                if response.ok:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Recover two paragraphs for each book,
                    # the first containing the link and the image,
                    # the second containing the link and the title
                    temporary_list = soup.find('ol', {'class': 'row'}).findAll('a')
                    # We put the links in keys and the title and image in value (in a list)
                    for i in range(int(len(temporary_list)/2)):
                        title = temporary_list[i*2+1]['title']
                        link = temporary_list[i*2]['href'].replace('../../..', 'https://books.toscrape.com/catalogue')
                        image = \
                            temporary_list[i*2].find('img')['src'].replace('../../../..', 'https://books.toscrape.com')
                        book_dictionary[link] = [title, image]
                else:
                    print(response)
    else:
        print(response)
    return book_dictionary
