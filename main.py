import csv
import os
import shutil
from slugify import slugify
from fonctions import *

category_dictionary = category_url_dictionary()  # Dictionary with category name (keys) and link (value)
# Creation of folders to tidy up the data
os.makedirs('csv_files', exist_ok=True)
os.makedirs('images', exist_ok=True)

for category, category_url in category_dictionary.items():
    print('Les données de la catégorie ' + category + ' sont en cours de récupération')
    os.makedirs('images/'+category, exist_ok=True)  # Creation of image folder for each category
    # Dictionary with book url (keys) title and picture link (value)
    book_dictionary = book_url_dictionary(category_url)
    with open('csv_files/'+category+'.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)  # initialization of the csv file
        writer.writerow(
            ['title'] + ['product_page_url'] + ['universal_ product_code (upc)'] + ['price_including_tax'] +
            ['price_excluding_tax'] + ['number_available'] + ['product_description'] + ['category'] +
            ['review_rating'] + ['image_url']
        )
        for link, values in book_dictionary.items():
            response = requests.get(link)
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                # get the product information table
                information_table = soup.find('table', {'class': 'table table-striped'})
                cell_list = information_table.findAll('td')  # list containing table cells
                upc = cell_list[0].text  # UPC number
                price_excluding_tax = cell_list[2].text.replace('Â', '')
                price_including_tax = cell_list[3].text.replace('Â', '')
                number_available = cell_list[5].text
                reviews = cell_list[6].text  # reviews number
                title = values[0]  # Title of the book
                image = values[1]  # picture link
                # get the description without the line breaks
                description = soup.find('meta', {'name': 'description'})['content'].strip()
                writer.writerow(
                    [title] + [link] + [upc] + [price_including_tax] + [price_excluding_tax] + [number_available] +
                    [description] + [category] + [reviews] + [image]
                )  # Addition of information in the csv
                r = requests.get(image, stream=True)  # download images
                if r.ok:
                    title = slugify(title, max_length=50)
                    with open('images/'+category+'/'+title+'.jpeg', 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else:
                    print(r)
            else:
                print(response)
        print('Les données de la catégorie ' + category + ' ont été récupérées')
