# RST Parser #

## 1. Required Package ##


```bash
wget https://repo.anaconda.com/archive/Anaconda2-2019.03-Linux-x86_64.sh
sh Anaconda2-2019.03-Linux-x86_64.sh
pip2 install sklearn
/home/intern/anaconda2/bin/pip install sklearn 

```

scipy, numpy, sklearn, nltk, python-tk 

The last two packages are required to draw the RST tree structure in the PostScript format. It is highly recommended to install these two packages for visualization. Otherwise, you have to read the bracketing results and to imagine what the tree looks like :-)

## 2. To run entire project together ##

Run the command "*python run.py "dplp" "tree"*"

First argument allows you to choose between using EDUs from DPLP or NeuralEDUSeg. To use NeuralEDUSeg EDUs, clone the repo github.com/ArnavParekhji/NeuralEDUSeg and place it in same folder as DPLP. Run by replacing "dplp" with "neu".

Second argument is to view the final relations in the form of a tree or json in streamlit. To view in json, replace "tree" with "json" and run.

## 3. RST Parsing with Raw Documents ##

To do RST parsing on raw documents, you will need syntactic parses and also the discourse segmentations on the documents. Let's start with preparing data

First, we need to collect all the documents into one folder, as all the following commands will scan this folder and process the documents in the same way. Let's assume the directory is **./data**

All the following commands will be run in a batch fasion, which means every command will scan will the documents in the data folder and process them once.

### 3.1 Data Processing ###

1. Run the Stanford CoreNLP with the given bash script **corenlp.sh** with the command "*./corenlp.sh path_to_dplp/data*"
    - This is a little awkward, as I am not sure how to call the Stanford parser from any other directory.

2. Convert the XML file into CoNLL-like format with command "*python convert.py ./data*"
    - Now, we can come back to the DPLP folder to run this command

### 3.2 Segmentation and Parsing ###

1. Segment each document into EDUs with command "*python segmenter ./data*"

2. Finally, run RST parser with command "*python rstparser ./data*"
    - The RST parser will generate the bracketing file for each document, which can be used for evaluation
    - It will also generate the PostScript file of the RST structure. Generating (and saving) these PS files will slow down the parsing procedure a little. You can turn it off with "*python rstparser ./data* False"


## 4. Training Your Own RST Parser ##

TODO

## Reference ##

Please read the following paper for more technical details

Yangfeng Ji, Jacob Eisenstein. *[Representation Learning for Text-level Discourse Parsing](http://jiyfeng.github.io/papers/ji-acl-2014.pdf)*. ACL 2014
