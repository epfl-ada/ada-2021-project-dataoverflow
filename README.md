# Quotations: China from a western perspective.

---
### Link to our datastory https://ruiarui.github.io/project-dataoverflow/

## Abstract

​    Over the years we have observed deteriorating relations between the US and China. In previous years we have seen escalating tensions as a result of the increasing trade deficit of the US with respect to China. More recently, the news has been dominated by the worldwide outbreak of Covid-19, for which some in the US blame China. It seems that often much of the opinions people hold find their origins with some public figure. Our research would therefore like to analyze the utterances of western public figures about China, as a reflection of the opinions of the general public. This research will therefore aim to provide an account of the changing relations as viewed from the western perspective. 

## Research Questions

The main research question we would like to answer is:

**What is the view of the western world on China?**

To answer this question, we propose the following sub-questions:

1. What main topics do western people associate China with?

​     We would like to analyze which topics western public figures present when talking about China. We think that this is a good first-shot method to gain insight into possible answers to the main research question, as they provide our later analyses with context about the relationship between the West and China. A possible finding might for example be that in 2020, the most frequent topic regarding China is Covid-19. This would then provide context to analysis between for example the view of different political parties.

2. How do these topics vary over time?

​    After extracting all the topics the western press associate China with, we analyze how these topics change over time. Will the topics change when big events happen? And will there be any topic that the press associate China with all the time?  This result will help us to connect our data with big events in these years.

3. What are the attitudes of the Western press towards these topics? Have these attitudes ever changed?

​    What interest us most is the attitudes these quotations show towards China. We believe that these quotes represent the attitude of the speakers and the media towards China, and to some extent, the views of the public towards China. For instance, there may be a negative attitude towards China in the quotations related to Covid-19. Again, we will attempt to analyze these attitudes as they change over time.

4. Do attitudes differ between different groups of speakers?

​    After focusing on the big picture, we want to look back to specific attributes of speakers. By combining data about the speakers in the dataset, we can see if there is any difference in different speaker groups? For example, attitudes from European countries and US may be different. In the US, Democrats may have more positive attitudes than Republicans. Female speakers may be more positive than male speakers.

## Datasets
` Quotebank Article-centric Dataset ` In order to obtain quotes about China, we need to filter the Quotebank dataset. However, we notice that there are many quotations that are related to China but do not contain any keywords like 'China' or 'Sino-'.  To have a more comprehensive and reasonable dataset, we decide to use the quotebank article-centric dataset to filter the data by checking whether the keywords are contained in the `leftContext`, `rightContext` or `quotation` rather than `quotation` alone, since the context around the quotation also matters to what the quotation is talking about. This sub-dataset will be therefore more reasonable and complete. 

` Wikidata `： To answer research question 4, we need more detailed information about each speaker. Thus, we intend to use Wikidata to get detailed information about speakers like gender, age,  nationality, party affiliation, etc for further analysis.

## Methods

#### Data Cleaning and Initial Analysis 

The first step of data cleaning is to extract the quotations related to China. We filter data by setting white-list keywords and filtering the quotations and the context of  articles in ` Quotebank Article-centric Dataset `. Then we drop the columns ` URLs, phase, article length `, which are not related to our research. We also perform an initial analysis to find abnormalities in the data. We can then use these abnormalities in order to find rows that need to be removed.

#### Topic and Keyword Extraction 

To answer research questions 1 and 2, we need to extract the keywords of the data. We use KeyBERT, a minimal keyword extraction technique that leverages BERT embeddings to create keywords and key phrases that are most similar to a sentence. We will apply KeyBERT to the title and quotation column and classify the quotes into keyword groups based on the title of the article in which they appear. We obtain a classification of keywords into meaningful topics, by labeling a small subset of keywords (top 50 occurring keywords per year) and bootstrapping a larger dataset. The idea behind it is that we have 5 keywords per quotation, we then hand label the top 50 keywords, and assume keywords in a list with a hand-labelled keyword belong to the same topic. We then label all keywords that occur only once in the dataset of one year as outliers if they do not appear with one of the top 50 keywords. We then train a RandomForestClassifier + PCA to predict the labels. Finally, we predict on all the keywords and take those as the topic labels.

#### Sentiment Analysis 

The following step of our project will be to analyse the attitude of the speaker as demonstrated by each quotation. We will use ` Twitter-roBERTa-base ` for our sentiment analysis. This is a roBERTa-base model trained on ~58M tweets and finetuned for sentiment analysis with the TweetEval benchmark. We apply this model and expect an attitude like `Positive`, `Negative` or `neutral` as the outcome.  After that, we can group the result to see what is the attitude on different topics, and the difference in gender, age, nationality, party affiliation, etc. We chose to use the twitter model, as quotations may be similar to these, as usually quotations are short and likely contain an opinion about a certain topic.



## Milestones and Proposed timeline
|  Date |  Task    |  Completion    |
| ---- | ---- | ---- |
|  By Week 8 (Milestone 2 Due)   | Finish initial assumptions. Get a sub-dataset from extraction and cleaning the `quotebank-2020.json.bz2`. Try some initial analysis. Verify the feasibility of subsequent steps on sub-dataset. | :heavy_check_mark: |
|  By Week 10 (HW2 Due)   |   Finish extraction and cleaning of the whole dataset. Finish topic extraction.   |  :heavy_check_mark:  |
|  By week 11    | Finish sentiment analysis. Draw some initial conclusions of the big picture. |  :heavy_check_mark:    |
|  By week 12   | Do deeper analysis and visualizations on each of the above research topics. |   :heavy_check_mark:   |
|  By week 13 (Milestone 3 Due)  |   Finalize the conclusions. Finish the notebook and the Readme file. Present our data story on a GitHub webpage.   |  :heavy_check_mark:    |




## Team Organization
@Bonan: Pre-process datasets, Analyse topic extraction result, Data visualization, Finalize the conclusions

@Jozef: Evaluate model performance, Topic extraction, Analyse sentiment analysis result, Finalize the conclusions, Present data, Topic extraction, Keyword classification

@Rui: Data wrangling, Initial data analysis, Sentiment analysis, Data visualization, Finalize the conclusions

@Yurui: Initial data analysis, Topic extraction, Data visualization, Finalize the conclusions, write project story





---



### Code Architecture
```
├── Initial_Analysis.ipynb: Our initial analysis notebook contains data cleaning and EDA
├── ML-Pipeline.ipynb: The machine learning pipeline implements the keyword exaction and sentiment analysis 
├── README.md
├── Extract_kw_labels_RQ3_part_1.ipynb, Topic_sentiment_RQ3_part_2.ipynb : Pipeline to answer question 3
├── data: the sub-dataset with data cleaning and analysis
├── notebooks: notebooks that contain our trying
│   ├── LDA.ipynb
│   └── firstTry.ipynb
└── src: python scripts that help deal with the data
    ├── data_cleaning.py
    └── data_extraction.py
```
