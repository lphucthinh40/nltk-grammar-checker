
import imp
import pickle
import sklearn_crfsuite
from sklearn.externals import joblib
from nltk.corpus import brown


# features generator for each sentence
def pos_features(sentence, i):
    current = sentence[i][0]

    # previous word
    if (i>0):
        prev_w = sentence[i-1][0]
    else:
        prev_w = "<START>"

    # next word
    if (i<len(sentence)-1):
        next_w = sentence[i+1][0]
    else:
        next_w = "<END>"

    # generate feature sets
    features = {
        "word": current,
        "next_word": next_w,
        "prev_word": prev_w,
        "suffix(1)": current[-1:],
        "suffix(2)": current[-2:],
        "suffix(3)": current[-3:],
        "prefix(1)": current[0],
        "prefix(2)": current[:2],
        "prefix(3)": current[:3],
        "prev_suffix(1)": prev_w[-1:],
        "prev_suffix(2)": prev_w[-2:],
        "prev_suffix(3)": prev_w[-3:],
        "prev_prefix(1)": prev_w[0],
        "prev_prefix(2)": prev_w[:2],
        "prev_prefix(3)": prev_w[:3],
        "next_suffix(1)": next_w[-1:],
        "next_suffix(2)": next_w[-2:],
        "next_suffix(3)": next_w[-3:],
        "next_prefix(1)": next_w[0],
        "next_prefix(2)": next_w[:2],
        "next_prefix(3)": next_w[:3],
        'is_first': i == 0,
        'is_last': i == len(sentence) - 1,
        'curr_is_title': current.istitle(),
        'prev_is_title': prev_w.istitle(),
        'next_is_title': next_w.istitle(),
        'curr_is_lower': current.islower(),
        'prev_is_lower': prev_w.islower(),
        'next_is_lower': next_w.islower(),
        'curr_is_upper': current.isupper(),
        'prev_is_upper': prev_w.isupper(),
        'next_is_upper': next_w.isupper(),
        'curr_is_digit': current.isdigit(),
        'prev_is_digit': prev_w.isdigit(),
        'next_is_digit': next_w.isdigit()
    }
    return features


# feature generator for dataset
def transformDatasetSequence(sentences):
    wordFeatures, wordLabels = [], []
    for sent in sentences:
        feats, labels = [], []
        for i in range(len(sent)):
            feats.append(pos_features(sent, i))
            labels.append(sent[i][1])
        wordFeatures.append(feats)
        wordLabels.append(labels)
    return wordFeatures, wordLabels


brown_tagged_sents = brown.tagged_sents(categories='news')
size = int(len(brown_tagged_sents) * 0.8)
train_sents = brown_tagged_sents[:size]
test_sents = brown_tagged_sents[size:]
trainSeqFeatures, trainSeqLabels = transformDatasetSequence(train_sents)
testSeqFeatures, testSeqLabels = transformDatasetSequence(test_sents)


def trainCRF(trainFeatures, trainLabels):
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True,
    )
    crf.fit(trainFeatures, trainLabels)
    return crf


crf_model = trainCRF(trainSeqFeatures[:30000], trainSeqLabels[:30000])

joblib.dump(crf_model, 'POStagger.joblib')
crf = joblib.load('POStagger.joblib')
print(crf.score(testSeqFeatures, testSeqLabels))
