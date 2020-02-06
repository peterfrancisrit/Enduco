import pandas as pd
import numpy as np
import re
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv(open('results.txt','rU'), encoding='utf-8', engine='c',sep='\0',header=None)
data[1].fillna('',inplace=True)
# get rid of similar intro
data['processed'] = data[1].apply(lambda x: x.replace('Joining VeloClub not only supports the work we do, there are some fantastic benefits:',''))
# Remove punctuation
data['processed'] = data['processed'].map(lambda x: re.sub('''[,“#\.!?”—@…*-:\";‘’\[\]\(\)|]''', '', x))
#  the titles to lowercase
data['processed'] = data['processed'].map(lambda x: x.lower())
# Print out the first rows of papers
data['processed'].head()

count_vectorizer = TfidfVectorizer(stop_words='english')
# Fit and transform the processed titles
count_data = count_vectorizer.fit_transform(data['processed'])

from sklearn.decomposition import LatentDirichletAllocation as LDA
# Tweak the two parameters below
number_topics = 10
number_words = 10
# Create and fit the LDA model
lda = LDA(n_components=number_topics, n_jobs=-1)
lda.fit(count_data)

LDAvis_prepared = sklearn_lda.prepare(lda, count_data, count_vectorizer)
pyLDAvis.save_html(LDAvis_prepared, './ldavis_prepared_'+ str(number_topics) +'.html')
