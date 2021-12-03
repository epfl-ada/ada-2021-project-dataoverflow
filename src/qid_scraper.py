import requests
from tqdm import tqdm
import numpy as np

QIDS = ['Q' + str(x) for x in range(100, 200)]
labels = []
batch_size = 20

for QID in tqdm(np.array_split(QIDS, len(QIDS) // batch_size)):
    querry = ''.join([q + '|' for q in QID])
    url = f'https://www.wikidata.org/w/api.php?action=wbgetentities&pops=labels&ids={querry[:-1]}'
    r = requests.get(url, params = {'format': 'json'})
    data = r.json()

    for q in QID:
        if 'labels' in data['entities'][q].keys():
            label = data['entities'][q]['labels']['en-gb']['value']
        else:
            label = None


        labels.append(label)

print(labels)






