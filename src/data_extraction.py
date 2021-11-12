import bz2
import json

'''
This python file is used to extract the dataset from article-centric quotabank data-sets.
The detailed reasons why we filter like the following can be found in `Initial_Analysis.ipynb`
'''

for year in range(2008, 2021):
    word_list = ['jinping xi', 'xi jing ping', 'xi jinping', 'president xi',
                 'china', 'chinese', 'beijing', 'peking', 'sino-']
    path_to_file = 'data/quotebank-'+str(year)+'.json.bz2'
    path_to_out = 'data/quotebank-'+str(year)+'-context-contains-related.json.bz2'
    

    with bz2.open(path_to_out, 'wb') as d_file:
        with bz2.open(path_to_file, 'rb') as s_file:
            for i, instance in enumerate(s_file):
                instance = json.loads(instance)
                if i % 10000 == 0:
                    print(i)
                for quote in instance['quotations']:
                    if quote['localTopSpeaker'] == 'None':
                        continue
                    if any(w in quote['quotation'].lower() for w in word_list):
                        quote['title'] = instance['title']
                        quote['date'] = instance['date']
                        quote['articleID'] = instance['articleID']
                        for name in instance['names']:
                            if name['name'] == quote['localTopSpeaker']:
                                quote['localTopSpeakerID'] = name['ids'].lstrip("[").rstrip("]").split(",")
                                break
                        d_file.write((json.dumps(quote) + '\n').encode('utf-8'))

                    elif any(w in quote['leftContext'].lower() for w in word_list):
                        quote['title'] = instance['title']
                        quote['date'] = instance['date']
                        quote['articleID'] = instance['articleID']
                        for name in instance['names']:
                            if name['name'] == quote['localTopSpeaker']:
                                quote['localTopSpeakerID'] = name['ids'].lstrip("[").rstrip("]").split(",")
                                break
                        d_file.write((json.dumps(quote) + '\n').encode('utf-8'))

                    elif any(w in quote['rightContext'].lower() for w in word_list):
                        quote['title'] = instance['title']
                        quote['date'] = instance['date']
                        quote['articleID'] = instance['articleID']
                        for name in instance['names']:
                            if name['name'] == quote['localTopSpeaker']:
                                quote['localTopSpeakerID'] = name['ids'].lstrip("[").rstrip("]").split(",")
                                break
                        d_file.write((json.dumps(quote) + '\n').encode('utf-8'))



