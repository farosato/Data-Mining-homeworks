import csv
import nltk
import os.path
import re
from bs4 import BeautifulSoup
from os import listdir

#SRC = './recipes'
SRC = './recipes_test'
DEST = './recipes.tsv'
DEST_PREP = './recipes-prep.tsv'
CODEC = 'utf-8'
HEADERS_LINE = ['title','author','prep_time','cook_time','num_people','dietary_info','ingredients','method']

# put recipes in a single .tsv file
with open(DEST, 'wb') as out:
    tsvWriter = csv.writer(out, delimiter='\t')
    tsvWriter.writerow(HEADERS_LINE)
    
    for f in listdir(SRC):
        row = []
        fid = open(os.path.join(SRC, f), 'r')
        recipeSoup = BeautifulSoup(fid, 'html.parser')
        
        for title in recipeSoup.find_all('h1', class_='content-title__text'):
            row.append(title.text.strip().encode(CODEC))
        
        for author in recipeSoup.find_all('a', class_='chef__link', itemprop='author'):
            row.append(author.text.strip().encode(CODEC))
        
        for prep_time in recipeSoup.find_all('p', class_='recipe-metadata__prep-time'):
            row.append(prep_time.text.strip().encode(CODEC))
        
        for cook_time in recipeSoup.find_all('p', class_='recipe-metadata__cook-time'):
            row.append(cook_time.text.strip().encode(CODEC))
        
        for serving in recipeSoup.find_all('p', class_='recipe-metadata__serving'):
            row.append(serving.text.strip().encode(CODEC))
        
        dietary = recipeSoup.find_all('p', class_='recipe-metadata__dietary-vegetarian-text')
        for d in dietary:
            row.append(d.text.strip().encode(CODEC))
        else:
            if len(dietary) == 0:
                row.append(''.encode(CODEC))
        
        ingredients = []
        for i in recipeSoup.find_all('li', class_='recipe-ingredients__list-item'):
            ingredients.append(i.text.strip())
        row.append(" | ".join(ingredients).encode(CODEC))
        
        method = []
        for m in recipeSoup.find_all('p', class_='recipe-method__list-item-text'):
            method.append(m.text.strip())
        row.append(" ".join(method).encode(CODEC))
        
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
        outRow.append(row[0])
        outRow.append(row[1])
        
        # TODO: include other fields
        for field in row[2:3]:
            #tokenizaton & stopwords removal
            tokens = [word for word in nltk.word_tokenize(field) if word not in stops]
            
            #stemming
            tokens = [stemmer.stem(t) for t in tokens]
            
            print tokens
            outRow.append(" ".join(tokens).encode(CODEC))
        
        tsvWriter.writerow(outRow)
            

    tsv.close()










