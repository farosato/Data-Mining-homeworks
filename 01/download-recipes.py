import re
import urllib2
from bs4 import BeautifulSoup

DEST = './recipes.txt'
SITEMAP_URL = 'http://www.bbc.co.uk/food/sitemap.xml'
RECIPE_REGEX = 'recipes\/'

if __name__ == "__main__":
    sitemap = urllib2.urlopen(SITEMAP_URL)
    sitemapSoup = BeautifulSoup(sitemap.read(), 'xml')
    
    i = 0
    with open(DEST, 'w') as out:
        for recipe in sitemapSoup.find_all('loc', string=re.compile(RECIPE_REGEX)):
            out.write(recipe.text+'\n')
            i+=1
        print str(i) + ' recipes retrieved.'
