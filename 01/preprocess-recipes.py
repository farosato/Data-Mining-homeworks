import os.path
from os import listdir
import nltk
import unicodecsv as csv
from bs4 import BeautifulSoup

# SRC = './recipes'
SRC = './recipes_test'
DEST = './recipes.tsv'
DEST_PREP = './recipes-prep.tsv'
HEADERS_LINE = ['title', 'author', 'prep_time', 'cook_time', 'num_people', 'dietary_info', 'ingredients', 'method']

# parse recipes and put data in a single .tsv file
with open(DEST, 'wb') as out:
    tsvWriter = csv.writer(out, delimiter='\t')
    tsvWriter.writerow(HEADERS_LINE)

    for f in listdir(SRC):
        print f
        row = []
        fid = open(os.path.join(SRC, f), 'r')
        recipeSoup = BeautifulSoup(fid, 'html.parser')

        for title in recipeSoup.find_all('h1', class_='content-title__text'):
            row.append(title.text.strip())

        for author in recipeSoup.find_all('a', class_='chef__link', itemprop='author'):
            row.append(author.text.strip())

        for prep_time in recipeSoup.find_all('p', class_='recipe-metadata__prep-time'):
            row.append(prep_time.text.strip())

        for cook_time in recipeSoup.find_all('p', class_='recipe-metadata__cook-time'):
            row.append(cook_time.text.strip())

        for serving in recipeSoup.find_all('p', class_='recipe-metadata__serving'):
            row.append(serving.text.strip())

        dietary = recipeSoup.find_all('p', class_='recipe-metadata__dietary-vegetarian-text')
        for d in dietary:
            row.append(d.text.strip())
        else:
            if len(dietary) == 0:
                row.append('')

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
stops = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.stem.porter.PorterStemmer()

with open(DEST_PREP, 'wb') as out:
    tsvWriter = csv.writer(out, delimiter='\t')
    tsvWriter.writerow(HEADERS_LINE)

    tsv = open(DEST, 'rb')
    tsvReader = csv.reader(tsv, delimiter='\t')

    next(tsvReader)
    for row in tsvReader:
        outRow = []

        # do not pre-process title and author
        outRow.append(row[0])
        outRow.append(row[1])

        for field in row[2:]:
            # TODO: ask if sent_tokenize is necessary for 'method' field
            # tokenizaton & stopwords removal
            tokens = [word for word in nltk.word_tokenize(field) if word not in stops]

            # stemming
            tokens = [stemmer.stem(t) for t in tokens]

            # print tokens
            outRow.append(" ".join(tokens))

        tsvWriter.writerow(outRow)

    tsv.close()
