import os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_log_Jul95.txt')
DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_log_prep.txt')


if __name__ == '__main__':
    with open(DEST, 'w') as dest:
        src = open(SRC, 'r')

        line = src.readline()
        while line != '':
            ip_addr = line.split('- -')[0].strip()
            dest.write(ip_addr + '\n')
            line = src.readline()

        src.close()
