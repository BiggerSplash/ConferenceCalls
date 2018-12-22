### Conference call transcript processing pipeline
Simple example pipeline for processing raw corporate earnings call transcripts from the Thomson Reuters StreetEvents database:

1. Parse metadata and use to filter based on characteristics in
matched sample in for example Compustat/WRDS.
2. Parse individual transcripts into interjection level flat files (primary key: `EventId` in `ccs/transcripts/output`)
3. Build corpus.
4. Do some computational linguistic on corpus (LDA for example).

### How
1. Install requirements: `$ pip install -r requirements.txt`
2. Run Make: `$ make`

### Example
```python
from sklearn.externals import joblib

# from sklearn:
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

lda = joblib.load('lda/output/lda.pkl')
countvec = joblib.load('lda/output/countvec.pkl')

print_top_words(lda, countvec.get_feature_names(), 5)
Topic #0: uk impella clients patients security
Topic #1: store gazprom neptune aid rite
Topic #2: oak ok pro forma imaging
Topic #3: fred food square feet miller
Topic #4: steel cvs lvs ph west
Topic #5: wireless stores store mobile devices
Topic #6: fusion ltx downturn ondemand hf
Topic #7: loan crores aetna webct health
Topic #8: california sensors solar phase underwriting
Topic #9: patient mobile patients political pt
```
