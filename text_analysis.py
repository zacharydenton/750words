#!/usr/bin/env python
# text analysis module
from collections import defaultdict

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def word_feats(words):
    return dict([(word, True) for word in words])

def get_words(textfile):
    try:
        for line in open(textfile):
            for word in line.split():
                yield word
    except:
        pass

def word_count(textfile):
    words = 0
    try:
        for line in open(textfile):
            for word in line.split():
                words += 1
    except:
        pass
    return words

def histogram(textfile):
    histo = defaultdict(int)
    for line in open(textfile):
        for word in line.split():
            word = word.lower()
            histo[word] += 1
    return histo

def classify_sentiment(textfile):
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
     
    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
     
    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4
     
    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

    words = word_feats(get_words(textfile))
     
    classifier = NaiveBayesClassifier.train(trainfeats)
    return classifier.classify(words)

def analyze(textfile):
    analysis = {}
    analysis['word_count'] = word_count(textfile)
    analysis['histogram'] = histogram(textfile)
    analysis['sentiment'] = classify_sentiment(textfile)
    return analysis

if __name__ == "__main__":
    import sys
    for textfile in sys.argv[1:]:
        print analyze(textfile)
