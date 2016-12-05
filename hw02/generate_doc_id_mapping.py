""" Script for displaying docs and doc_id mapping """
import __init__  # update Python PATH
import os
from hw01.list_recipes import DEST as SRC


DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapping.txt')


if __name__ == "__main__":
    with open(DEST, 'w') as dest:
        src = open(SRC, 'r')

        doc_id, line = 0, src.readline()
        while line != '':
            dest.write('{0: <7}'.format(doc_id) + line)
            doc_id, line = doc_id + 1, src.readline()

        src.close()
