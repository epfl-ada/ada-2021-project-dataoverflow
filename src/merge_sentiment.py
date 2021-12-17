import pandas as pd

# extract the sentiment and speaker attributes from all years

mycolumns=['quoteID','articleID','date','id','nationality',
       'gender', 'lastrevid', 'ethnic_group', 'US_congress_bio_ID',
       'occupation', 'party', 'academic_degree', 'religion',
           'negative_sentiment', 'neutral_sentiment', 'positive_sentiment', 'max_sentiment']

df_2008 = pd.read_json('D:/zproject/new/processed_western_quotes_2008.json.bz2')
western_sentiment=df_2008[mycolumns]
print(western_sentiment.shape)

for year in range(2009,2019):
    print(western_sentiment.shape)
    df_year = pd.read_json('D:/zproject/new/processed_western_quotes_'+str(year)+'.json.bz2')
    western_sentiment = pd.concat([western_sentiment,df_year[mycolumns]])
    
for i in range(1,5):
    print(western_sentiment.shape)
    df_year = pd.read_json('D:/zproject/new/processed_western_quotes_2019-'+str(i)+'.json.bz2')
    western_sentiment = pd.concat([western_sentiment,df_year[mycolumns]])

print(western_sentiment.shape)
df_year = pd.read_json('D:/zproject/new/processed_western_quotes_2020.json.bz2')
western_sentiment = pd.concat([western_sentiment,df_year[mycolumns]])
print(western_sentiment.shape)

western_sentiment.reset_index().drop(columns=['index']).to_json('D:/zproject/new/western_sentiment.json.bz2')