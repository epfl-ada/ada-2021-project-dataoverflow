import pandas as pd

'''
This python file is used for cleaning extracted datasets. 
The detailed reasons why we do each step can be found in `Initial_Analysis.ipynb`.
'''

max_length_title = 200
speaker_df = pd.read_parquet('data/speaker_attributes.parquet')
western_countries = pd.read_csv('data/western_countries_list.csv')

for year in range(2008, 2021):
    file_name = 'data/quotebank-{}-context-contains-related.json.bz2'.format(year)
    china_df = pd.read_json(file_name ,lines=True)

    # Filter rows with very long titles
    china_df = china_df[china_df['title'].apply(len)<=max_length_title]

    # Drop rows without speaker ids
    china_df = china_df.dropna(axis=0, subset=["localTopSpeakerID"])

    # Keep rows with only one speaker id
    china_df = china_df[china_df.localTopSpeakerID.apply(len)==1]
    china_df.localTopSpeakerID = china_df.localTopSpeakerID.apply(lambda x:x[0])

    # Merge the speaker information into the quotation table on the speaker id
    merged_df = china_df.merge(speaker_df, left_on='localTopSpeakerID', right_on='id', how = 'left')

    # Drop rows without nationality
    merged_df = merged_df[~merged_df['nationality'].isna()]

    # Keep rows where speakers' nationalities are of western countries
    western_df = merged_df[merged_df['nationality'].apply(lambda x: any(y in western_countries['QID'].to_list() for y in x))]

    # Save cleaned data back to files
    western_df.to_json("data/western-quotes-{}.json.bz2".format(year), lines=True, orient="records")