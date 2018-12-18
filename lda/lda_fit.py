import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.externals import joblib

corpus = pd.read_csv('../corpus/output/corpus.csv')

countvec_pre = CountVectorizer(analyzer=str.split)
tfidf = TfidfTransformer()

bow_pre = countvec_pre.fit_transform(corpus['speech_t'])
tfidf.fit(bow_pre)

# Remove very frequent or very rare tokens
lower = np.percentile(tfidf.idf_, 10)
upper = np.percentile(tfidf.idf_, 90)
remove = np.where((tfidf.idf_ < lower) | (tfidf.idf_ > upper))
words_remove = np.array(countvec_pre.get_feature_names())[remove]

countvec = CountVectorizer(analyzer='word',
                           tokenizer=str.split,
                           stop_words=list(words_remove))
# Final bag of words
bow = countvec.fit_transform(corpus['speech_t'])

# Plain 10-topic model
lda = LatentDirichletAllocation()
lda.fit(bow)

# Serialize
joblib.dump(countvec, 'output/countvec.pkl')
joblib.dump(lda, 'output/lda.pkl')
