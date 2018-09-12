## extractparsing.py
## Author: Yangfeng Ji
## Date: 02-10-2015
## Time-stamp: <yangfeng 09/25/2015 23:43:17>

from preprocess.xmlreader import reader, writer, combine
from os import listdir
from os.path import join

def extract(fxml):
    sentlist, constlist = reader(fxml)
    sentlist = combine(sentlist, constlist)
    fconll = fxml.replace(".xml", ".conll")
    writer(sentlist, fconll)

def main(rpath):
    files = [join(rpath,fname) for fname in listdir(rpath) if fname.endswith(".xml")]
    cnt = 10
    import multiprocessing
    pool = multiprocessing.Pool(processes=cnt)
    pool.map(extract, files)
    pool.close()
    pool.join()


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        main(rpath=sys.argv[1])
    else:
        print "python convert.py data_path"
