import sys, os

edu = sys.argv[1]
view = sys.argv[2]

os.system("./corenlp.sh ./data")
os.system("python convert.py ./data")
os.system("python segmenter ./data ./data \"" + edu + "\"")
os.system("streamlit run rstparser.py ./data True \"" + view + "\"")