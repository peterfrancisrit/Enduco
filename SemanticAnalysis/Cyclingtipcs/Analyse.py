from pandas import DataFrame as df
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation as LDA
from pyLDAvis import sklearn as sklearn_lda
import pickle
import pyLDAvis
import os
from pyfiglet import Figlet

class Analyse:

    def __init__(self, year_from,year_to, month_from, month_to, n_topics):
        self.year_from = year_from
        self.year_to = year_to
        self.month_from = month_from
        self.month_to = month_to
        self.n_topics = n_topics
        self.topic_output = 'topic_output.txt'

        # open and clean
        self._open()
        self._clean()
        self._model()


    def _model(self):
        # fit vectorizer and transform
        sub_data = self.data[(self.data.year >= self.year_from) & (self.data.year <= self.year_to)]
        sub_data = sub_data[(sub_data.month >= self.month_from) & (sub_data.month <= self.month_to)]

        self.vectorizer = TfidfVectorizer(stop_words='english').fit(sub_data.processed)
        self.tfidf_data = self.vectorizer.transform(sub_data.processed)

        # fit LDA
        self.model = LDA(n_components=self.n_topics, n_jobs=-1)
        self.model.fit(self.tfidf_data)

        # Print the topics found by the LDA model
        print("Topics found via LDA:")
        self.print_topics()

        print("Modelling...")
        LDAvis_prepared = sklearn_lda.prepare(self.model, self.tfidf_data, self.vectorizer,mds='mmds')
        pyLDAvis.save_html(LDAvis_prepared, './LDAvis_prepared_'+ str(self.n_topics) +'.html')

        del sub_data

    def _open(self):
        # Open and read
        assert os.path.exists('results.txt'), "Crawler must have data!"

        dates = []
        text = []

        with open('results.txt','r') as file:
            lines = file.readlines()
            for line in lines:
                dates.append(line.split('\0')[0])
                text.append(line.split('\0')[1])
            file.close()

        self.data = pd.df({'date': dates,'text':text})

    def _clean(self):
        ''' Cleans the data, removing nans, removing stop words, lower case, removes punctuation'''

        # clean data
        self.data['text'].fillna('',inplace=True)
        # get rid of similar intro
        self.data['processed'] = self.data['text'].apply(lambda x: x.replace('Joining VeloClub not only supports the work we do, there are some fantastic benefits:',''))
        # Remove punctuation
        self.data['processed'] = self.data['processed'].map(lambda x: re.sub('''[,“#\.!?”—@…*-:\";‘’\[\]\(\)|]''', '', x))
        #  the titles to lowercase
        self.data['processed'] = self.data['processed'].map(lambda x: x.lower())
        # Print out the first rows of papers
        self.data['processed'].head()
        self.data['date'] = self.data['date'].apply(lambda x: "here is an error" if type(x) == float else x)
        self.data['date'] = self.data['date'].apply(lambda x: x if re.match(r"[A-Za-z]+ [0-9]+, [0-9]+", x) != None else 'OUT')
        data_clean = self.data[self.data['date'] != "OUT"]
        data_clean['time'] = pd.to_datetime(data_clean['date'], format="%B %d, %Y")
        data_clean['year'] = data_clean.time.dt.year
        data_clean['month'] = data_clean.time.dt.month
        data_clean = data_clean.set_index('time')
        self.data = data_clean

        del data_clean

    def print_topics(self):
        '''
        Prints the topics with top n words (n_top_words) in the topic:

            print_topics(LDAmodel, COUNT_VECTORIZER, 3)
            -> Topic 0: soap dish bowl
            -> Topic 1: rice eggs ham
            ...
        '''
        n_top_words = 10
        words = self.vectorizer.get_feature_names()
        for topic_idx, topic in enumerate(self.model.components_):
            print("\nTopic #%d:" % topic_idx, " ".join([words[i]
                            for i in topic.argsort()[:-n_top_words - 1:-1]]),file=open(self.topic_output,'a+'))

if __name__ == "__main__":
    X = Analyse(2009,2020,1,12,10)
