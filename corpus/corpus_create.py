# Create corpus from parsed speech
# aggregates to conference call section level
# stores tokenized (speech_t) and stemmed (speech_s) text

import pandas as pd
import nltk
from nltk.tokenize import RegexpTokenizer

FILE_PARSED_SPEECH = '../ccs/transcripts/output/speech.csv'
OUTPUT_FILE_CORPUS = 'output/corpus.csv'

# Same as sklearn default token pattern, but excluding numbers
tokenizer = RegexpTokenizer(r'(?u)\b[a-zA-Z_][a-zA-Z_]+\b')
port = nltk.PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english')

def tokenize(s, stopwords, tokenizer):
    tokens = tokenizer.tokenize(s)
    return ' '.join(
        [token.lower() for token in tokens if token not in stopwords])

def stem(s, stemmer):
    stemmed = [stemmer.stem(t) for t in s.split()]
    return ' '.join(stemmed)

# Main
df = pd.read_csv(FILE_PARSED_SPEECH)

# Remove interjection if no speech
# (example: EventId=3431374_T.xml: line 248)
df = df[~df['speech'].isna()]

# Aggregate to section level
df_agg = df.groupby(['Event.@Id', 'section'])['speech'].apply(
            lambda x: ' '.join(x)).reset_index()

# Tokenize
df_agg['speech_t'] = df_agg.apply(lambda row: tokenize(
        row['speech'], stopwords, tokenizer), axis=1)

# Stem
df_agg['speech_s'] = df_agg.apply(lambda row: stem(
        row['speech_t'], port), axis=1)

df_agg[['Event.@Id', 'section', 'speech_t', 'speech_s']].to_csv(
        OUTPUT_FILE_CORPUS, index=False, na_rep='NA')
