## evalparser.py
## Author: Yangfeng Ji
## Date: 11-05-2014
## Time-stamp: <yangfeng 09/25/2015 16:32:42>

# modified by Jiacheng Xu

from model import ParsingModel
from tree import RSTTree
from docreader import DocReader
from evaluation import Metrics
from os import listdir
from os.path import join as joinpath
from util import drawrst
import multiprocessing

global_pm = None
global_bv = None


def parse(pm, doc):
    """ Parse one document using the given parsing model

    :type pm: ParsingModel
    :param pm: an well-trained parsing model

    :type fedus: string
    :param fedus: file name of an document (with segmented EDUs) 
    """
    pred_rst = pm.sr_parse(doc)
    return pred_rst


def writebrackets(fname, brackets):
    """ Write the bracketing results into file
    """
    print('Writing parsing results into file: {}'.format(fname))
    with open(fname, 'w') as fout:
        for item in brackets:
            fout.write(str(item) + '\n')


def eval_parser_unit(fmerge, bcvocab=None, pm=None, draw=False):
    bcvocab = global_bv
    pm = global_pm
    assert bcvocab is not None
    assert pm is not None
    dr = DocReader()
    doc = dr.read(fmerge)
    # ----------------------------------------
    # Parsing
    pred_rst = pm.sr_parse(doc, bcvocab)
    if draw:
        strtree = pred_rst.parse()
        drawrst(strtree, fmerge.replace(".merge", ".ps"))
    # Get brackets from parsing results
    pred_brackets = pred_rst.bracketing()
    fbrackets = fmerge.replace('.merge', '.brackets')
    # Write brackets into file
    writebrackets(fbrackets, pred_brackets)
    # ----------------------------------------
    # Evaluate with gold RST tree
    # if report:
    #     fdis = fmerge.replace('.merge', '.dis')
    #     gold_rst = RSTTree(fdis, fmerge)
    #     gold_rst.build()
    #     gold_brackets = gold_rst.bracketing()
    #     met = Metrics(levels=['span', 'nuclearity', 'relation'])
    #     met.eval(gold_rst, pred_rst)


def evalparser(path='./examples', report=False,
               bcvocab=None, draw=True,
               withdp=False, fdpvocab=None, fprojmat=None):
    """ Test the parsing performance

    :type path: string
    :param path: path to the evaluation data

    :type report: boolean
    :param report: whether to report (calculate) the f1 score
    """
    # ----------------------------------------
    # Load the parsing model
    print('Load parsing model ...')
    pm = ParsingModel(withdp=withdp,
                      fdpvocab=fdpvocab, fprojmat=fprojmat)
    pm.loadmodel("model/parsing-model.pickle.gz")
    # ----------------------------------------
    # Evaluation
    met = Metrics(levels=['span', 'nuclearity', 'relation'])
    # ----------------------------------------
    # Read all files from the given path
    exsisting_files = [ ".".join(  fname.split(".")[:-1]) for fname in listdir(path) if fname.endswith('.brackets')]
    all_files = [ ".".join(fname.split(".")[:-1])  for fname in listdir(path) if fname.endswith('.merge')]
    todo_files = list(set(all_files) - set(exsisting_files))
    doclist = [joinpath(path, fname + '.merge') for fname in todo_files]
    print("TODO files len:")
    print(len(doclist))
    print(doclist[0])
    global_pm = pm
    global global_pm
    global_bv = bcvocab
    global global_bv
    eval_parser_unit(doclist[0])
    cnt = multiprocessing.cpu_count()

    pool = multiprocessing.Pool(processes=cnt)

    pool.map(eval_parser_unit, doclist)
    pool.close()
    pool.join()
    """
    for fmerge in doclist:
        # ----------------------------------------
        # Read *.merge file
        dr = DocReader()
        doc = dr.read(fmerge)
        # ----------------------------------------
        # Parsing
        pred_rst = pm.sr_parse(doc, bcvocab)
        if draw:
            strtree = pred_rst.parse()
            drawrst(strtree, fmerge.replace(".merge", ".ps"))
        # Get brackets from parsing results
        pred_brackets = pred_rst.bracketing()
        fbrackets = fmerge.replace('.merge', '.brackets')
        # Write brackets into file
        writebrackets(fbrackets, pred_brackets)
        # ----------------------------------------
        # Evaluate with gold RST tree
        if report:
            fdis = fmerge.replace('.merge', '.dis')
            gold_rst = RSTTree(fdis, fmerge)
            gold_rst.build()
            gold_brackets = gold_rst.bracketing()
            met.eval(gold_rst, pred_rst)
    if report:
        met.report()
    """
