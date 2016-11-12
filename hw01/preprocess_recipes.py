import unicodecsv as csv
import preprocessing
from store_recipes import HEADER_LINE
from store_recipes import DEST as SRC
import time
import os.path

DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipes-prep.tsv')

if __name__ == "__main__":
    start_time = time.time()

    with open(DEST, 'wb') as out:
        tsvWriter = csv.writer(out, delimiter='\t')
        tsvWriter.writerow(HEADER_LINE)

        tsv = open(SRC, 'rb')
        tsvReader = csv.reader(tsv, delimiter='\t')

        next(tsvReader)  # skip header line
        for row in tsvReader:
            outRow = []

            for field in row[:-1]:  # ignore the url field
                tokens = preprocessing.preprocess(field)
                outRow.append(" ".join(tokens))

            tsvWriter.writerow(outRow)

        tsv.close()

    print("\n--- %s seconds ---" % (time.time() - start_time))