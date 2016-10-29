import os.path
from os import listdir
import unicodecsv as csv
from bs4 import BeautifulSoup
import preprocessing

# SRC = './recipes'
SRC = './recipes_test'
DEST = './recipes.tsv'
DEST_PREP = './recipes-prep.tsv'
HEADER_LINE = ['title', 'author', 'prep_time', 'cook_time', 'num_people', 'dietary_info', 'description', 'ingredients', 'method']

# parse recipes and put data in a single .tsv file
with open(DEST, 'wb') as out:
    tsvWriter = csv.writer(out, delimiter='\t')
    tsvWriter.writerow(HEADER_LINE)

    for f in listdir(SRC):
        print f
        row = []
        fid = open(os.path.join(SRC, f), 'r')
        recipeSoup = BeautifulSoup(fid, 'html.parser')

        try: row.append(recipeSoup.find('h1', class_='content-title__text').text.strip())
        except AttributeError: row.append('')

        try: row.append(recipeSoup.find('a', class_='chef__link', itemprop='author').text.strip())
        except AttributeError: row.append('')

        try: row.append(recipeSoup.find('p', class_='recipe-metadata__prep-time').text.strip())
        except AttributeError: row.append('')

        try: row.append(recipeSoup.find('p', class_='recipe-metadata__cook-time').text.strip())
        except AttributeError: row.append('')

        try: row.append(recipeSoup.find('p', class_='recipe-metadata__serving').text.strip())
        except AttributeError: row.append('')

        try: row.append(recipeSoup.find('p', class_='recipe-metadata__dietary-vegetarian-text').text.strip())
        except AttributeError: row.append('')

        try: row.append(recipeSoup.find('p', class_='recipe-description__text').text.strip())
        except AttributeError: row.append('')

        ingredients = []
        for i in recipeSoup.find_all('li', class_='recipe-ingredients__list-item'):
            ingredients.append(i.text.strip())
        row.append(" | ".join(ingredients))

        method = []
        for m in recipeSoup.find_all('p', class_='recipe-method__list-item-text'):
            method.append(m.text.strip())
        row.append(" ".join(method))

        tsvWriter.writerow(row)
        fid.close()

# pre-processing
with open(DEST_PREP, 'wb') as out:
    tsvWriter = csv.writer(out, delimiter='\t')
    tsvWriter.writerow(HEADER_LINE)

    tsv = open(DEST, 'rb')
    tsvReader = csv.reader(tsv, delimiter='\t')

    next(tsvReader) # skip header line
    for row in tsvReader:
        outRow = []

        for field in row:
            tokens = preprocessing.preprocess(field)
            outRow.append(" ".join(tokens))

        tsvWriter.writerow(outRow)

    tsv.close()
