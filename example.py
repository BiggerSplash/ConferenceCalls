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
