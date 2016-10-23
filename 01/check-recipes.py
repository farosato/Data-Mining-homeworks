import os.path

SRC = './recipes-names.txt'
PATH = 'C:/Users/Giacomo/Documents/Universita/Data_Mining/homeworks/01/recipes_old/'

with open(SRC, 'r') as fid:
    i = 0
    line = fid.readline().rstrip()
    while line is not "":
        if not os.path.isfile(os.path.join(PATH, line[:len(line)-1]+'.html')):
            print str(line).rstrip()
            i += 1
        line = fid.readline().rstrip()
        if i == 10:
            break
    print '\n' + str(i) + ' recipes not downloaded.'
