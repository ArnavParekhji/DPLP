## extractparsing.py
## Author: Yangfeng Ji
## Date: 02-10-2015
## Time-stamp: <yangfeng 09/25/2015 23:43:17>
import multiprocessing
from preprocess.xmlreader import reader, writer, combine
from os import listdir
from os.path import join


def extract(fxml):
    sentlist, constlist = reader(fxml)
    sentlist = combine(sentlist, constlist)
    fconll = fxml.replace(".xml", ".conll")
    writer(sentlist, fconll)


def main(rpath):
    exsisting_files = [join(rpath, fname) for fname in listdir(rpath) if fname.endswith(".conll")]
    exsisting_files_prefix = [".".join(x.split('.')[:-1]) for x in exsisting_files]
    all_files = [join(rpath, fname) for fname in listdir(rpath) if fname.endswith(".xml")]
    all_files_prefix = [".".join(x.split('.')[:-1]) for x in all_files]
    todo_files = list(set(all_files_prefix) - set(exsisting_files_prefix))
    files = [x + '.xml' for x in todo_files]
    print("Len of files todo {}".format(len(files)))
    cnt = multiprocessing.cpu_count()

    pool = multiprocessing.Pool(processes=cnt)
    pool.map(extract, files)
    pool.close()
    pool.join()


if __name__ == '__main__':
    import sys

    print("sys.argv[1] is the path")
    if len(sys.argv) == 2:
        main(rpath=sys.argv[1])
    else:
        print('python convert.py data_path')
