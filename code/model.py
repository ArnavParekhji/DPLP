## model.py
## Author: Yangfeng Ji
## Date: 09-09-2014
## Time-stamp: <yangfeng 09/27/2015 12:32:37>

""" As a parsing model, it includes the following functions
1, Mini-batch training on the data generated by the Data class
2, Shift-Reduce RST parsing for a given text sequence
3, Save/load parsing model
"""

from sklearn.svm import LinearSVC
# from cPickle import load, dump
from _pickle import load, dump
from code.parser import SRParser
from code.feature import FeatureGenerator
from code.tree import RSTTree
from code.util import *
# import code.util as util
from code.datastructure import ActionError
from operator import itemgetter
import gzip, sys

class ParsingModel(object):
    def __init__(self, vocab=None, idxlabelmap=None, clf=None, withdp=None, fdpvocab=None, fprojmat=None):
        """ Initialization
        
        :type vocab:
        :param vocab:

        :type idxrelamap:
        :param idxrelamap:

        :type clf:
        :param clf:
        """
        self.vocab = vocab
        # print labelmap
        self.labelmap = idxlabelmap
        if clf is None:
            self.clf = LinearSVC(C=1.0, penalty='l1',
                loss='squared_hinge', dual=False, tol=1e-7)
        else:
            self.clf = clf
        self.withdp = withdp
        self.dpvocab, self.projmat = None, None
        if withdp:
            print('Loading projection matrix ...')
            with gzip.open(fdpvocab) as fin:
                self.dpvocab = load(fin)
            with gzip.open(fprojmat) as fin:
                self.projmat = load(fin)
        print('Finish initializing ParsingModel')


    def train(self, trnM, trnL):
        """ Perform batch-learning on parsing model
        """
        print('Training ...')
        self.clf.fit(trnM, trnL)


    def predict(self, features):
        """ Predict parsing actions for a given set
            of features

        :type features: list
        :param features: feature list generated by
                         FeatureGenerator
        """
        vec = vectorize(features, self.vocab,
                        self.dpvocab, self.projmat)
        label = self.clf.predict(vec)
        # print label
        return self.labelmap[label[0]]


    def rank_labels(self, features):
        """ Rank the decision label with their confidence
            value
        """
        vec = vectorize(features, self.vocab,
                        self.dpvocab, self.projmat)
        vals = self.clf.decision_function(vec)
        # print vals.shape
        # print len(self.labelmap)
        labelvals = {}
        for idx in range(len(self.labelmap)):
            labelvals[self.labelmap[idx]] = vals[0,idx]
        sortedlabels = sorted(labelvals.items(), key=itemgetter(1),
                              reverse=True)
        labels = [item[0] for item in sortedlabels]
        return labels


    def savemodel(self, fname):
        """ Save model and vocab
        """
        if not fname.endswith('.gz'):
            fname += '.gz'
        D = {'clf':self.clf, 'vocab':self.vocab,
             'idxlabelmap':self.labelmap}
        with gzip.open(fname, 'w') as fout:
            dump(D, fout)
        print('Save model into file: {}'.format(fname))


    def loadmodel(self, fname):
        """ Load model
        """
        with gzip.open(fname, 'r') as fin:
        # with open(fname, 'rb') as fin:
            D = load(fin, encoding="latin1")
        self.clf = D['clf']
        self.vocab = D['vocab']
        self.labelmap = D['idxlabelmap']
        print('Load model from file: {}'.format(fname))


    def sr_parse(self, doc, bcvocab=None):
        """ Shift-reduce RST parsing based on model prediction

        :type texts: list of string
        :param texts: list of EDUs for parsing

        :type bcvocab: dict
        :param bcvocab: brown clusters
        """
        # raise NotImplementedError("Not finished yet")
        # Initialize parser
        srparser = SRParser([],[])
        srparser.init(doc)
        # Parsing
        while not srparser.endparsing():
            # Generate features
            stack, queue = srparser.getstatus()
            # Make sure call the generator with
            # same arguments as in data generation part
            fg = FeatureGenerator(stack, queue, doc, bcvocab)
            feat = fg.features()
            # label = self.predict(feat)
            labels = self.rank_labels(feat)
            for label in labels:
                action = label2action(label)
                try:
                    srparser.operate(action)
                    break
                except ActionError:
                    # print "Parsing action error with {}".format(action)
                    pass
        tree = srparser.getparsetree()
        rst = RSTTree()
        rst.asign_tree(tree)
        return rst
            
