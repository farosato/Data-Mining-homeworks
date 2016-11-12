import unicodecsv as csv
import preprocessing
from store_recipes import HEADER
from store_recipes import DEST as SRC
import time
import os.path

DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipes-prep.tsv')

if __name__ == "__main__":
    start_time = time.time()

    with open(DEST, 'wb') as out:
        tsv_writer = csv.writer(out, delimiter='\t', encoding='utf-8')
        tsv_writer.writerow(HEADER)

        tsv = open(SRC, 'rb')
        tsv_reader = csv.reader(tsv, delimiter='\t', encoding='utf-8')

        next(tsv_reader)  # skip header line
        for row in tsv_reader:
            outRow = []

            for field in row[:-1]:  # ignore the url field
                tokens = preprocessing.preprocess(field)
                outRow.append(" ".join(tokens))

            tsv_writer.writerow(outRow)

        tsv.close()

    print("\n--- %s seconds ---" % (time.time() - start_time))