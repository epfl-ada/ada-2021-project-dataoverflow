import pandas as pd
import os
import glob

folder = '/Users/alex/EPFL/ADA/project/processed-wq'

file = '/Users/alex/EPFL/ADA/project/processed-wq/processed_western_quotes_2020.json.bz2'

columns_qid = ['gender', 'ethnic_group', 'occupation', 'party', 'academic_degree', 'candidacy', 'religion']

files = []
os.chdir(folder)
for file in glob.glob("*.bz2"):
    files.append(file)
print(len(files))

pids_all = []

for f in files:
    df = pd.read_json(f)
    qids = []
    for col in columns_qid:
        ls = df.explode(column=col)[col]
        qids += ls.dropna().values.tolist()
    qids1 = list(dict.fromkeys(qids))
    print(f)
    print(len(qids1))
    pids_all += qids1
pids_all = list(dict.fromkeys(pids_all))
print(len(pids_all))

textfile = open("qids.txt", "w", encoding='utf-8')
for element in pids_all:
    textfile.write(element + "\n")
textfile.close()
