## main.py
## Author: Yangfeng Ji
## Date: 09-25-2015
## Time-stamp: <yangfeng 09/26/2015 00:10:59>

from code.evalparser import evalparser
# from cPickle import load
from _pickle import load
import gzip, sys

def main(path, draw=True, mode="tree"):
    with gzip.open("resources/bc3200.pickle.gz") as fin:
        print('Load Brown clusters for creating features ...')
        bcvocab = load(fin, encoding="latin1")
    evalparser(path=path, report=False, draw=draw,
               bcvocab=bcvocab,
               withdp=False, mode=mode)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[1]
        print('Read files from: {}'.format(path))
        main(path)
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        draw = eval(sys.argv[2])
        print('Read files from {}'.format(path))
        main(path, draw)
    elif len(sys.argv) == 4:
        path = sys.argv[1]
        draw = eval(sys.argv[2])
        mode = sys.argv[3].lower()
        print('Read files from {}'.format(path))
        main(path, draw, mode)
    else:
        print("Usage: python rstparser.py file_path [draw_rst_tree]")
        print("\tfile_path - path to the segmented file")

