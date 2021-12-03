from tqdm import tqdm
import numpy as np
import pandas as pd
import torch
from keybert import KeyBERT
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import urllib.request
from scipy.special import softmax
import csv
import warnings

root = 'C:/Users/jozef/Desktop/quotebank/'

task = 'sentiment'

MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
labels = []
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
labels = [row[1] for row in csvreader if len(row) > 1]

# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
model.save_pretrained(MODEL)
kw_model = KeyBERT()

years = ['2018', '2019']

for year in years:
    print('Working on year {}'.format(year))
    path = '{}western_quotes/western-quotes-{}.json.bz2'.format(root, year)
    quote_df = pd.read_json(path, lines=True)
    title_df = quote_df.drop_duplicates(subset='title')['title']

    print('Extracting keywords')

    warnings.filterwarnings('ignore')
    keywords = []
    batch_size = 200
    with torch.no_grad():
        for titles in tqdm(np.array_split(title_df, len(title_df) // batch_size)):
            keywords += kw_model.extract_keywords(titles.tolist(), stop_words='english')


    title_df = pd.DataFrame(title_df)
    title_df['keywords'] = keywords

    topic_df = quote_df.merge(title_df, on='title', how='left')

    topic_df = topic_df[topic_df.quotation.apply(len) <= 500]
    quotation_df = topic_df.drop_duplicates(subset='quotation')['quotation']

    model = model.to("cuda:0")
    print('Extracting sentiment')
    batch_size = 30
    quote_scores = np.array([])
    with torch.no_grad():
        for quote in tqdm(np.array_split(quotation_df, quotation_df.shape[0]//batch_size)):
            encoded_input = tokenizer(quote.tolist(), return_tensors='pt', padding=True).to("cuda:0")
            output = model(**encoded_input)
            scores = output[0].detach().cpu().numpy()
            scores = softmax(scores, axis=1)
            quote_scores = np.append(quote_scores, scores)
            del encoded_input, output

    torch.cuda.empty_cache()

    quotation_df = pd.DataFrame(quotation_df)
    quotation_df['quote_scores'] = list(quote_scores.reshape(-1, 3))

    complete_df = topic_df.merge(quotation_df, on='quotation', how='left')

    complete_df['negative_sentiment'] = [x[0] for x in complete_df['quote_scores']]
    complete_df['neutral_sentiment'] = [x[1] for x in complete_df['quote_scores']]
    complete_df['positive_sentiment'] = [x[2] for x in complete_df['quote_scores']]

    complete_df['max_sentiment'] = [labels[np.argmax(x)] for x in complete_df['quote_scores']]

    complete_df.drop('quote_scores', axis=1, inplace=True)

    complete_df = complete_df[complete_df['keywords'].apply(len) == 5]

    print('saving to file')
    complete_df.to_json('{}processed_western_quotes/processed_western_quotes_{}.json.bz2'.format(root, year))