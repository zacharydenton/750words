#!/usr/bin/env python
# text analysis module
from collections import defaultdict
import cPickle as pickle

import nltk

def word_feats(words):
    return dict([(word, True) for word in words])

def get_words(path):
    words = []
    for line in open(path):
        for word in line.split():
            if word.isalpha():
                words.append(word.lower())
    return words

def get_corpus(path=None):
    if path is None:
        try:
            from sevenfifty import SevenFiftyWords
            sevenfiftywords = SevenFiftyWords()
            path = sevenfiftywords.output_dir
        except:
            return
    return nltk.corpus.PlaintextCorpusReader(path, '.*')

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
            if word not in nltk.corpus.stopwords.words('english'):
                histo[word] += 1
    return histo

def classify_sentiment(textfile):
    words = word_feats(get_words(textfile))
    try:
        sentiment_file = open('.sentiment_classifier', 'rb')
        classifier = pickle.load(sentiment_file)
        sentiment_file.close()
    except:
        print "generating sentiment classifier..."

        negids = nltk.corpus.movie_reviews.fileids('neg')
        posids = nltk.corpus.movie_reviews.fileids('pos')
     
        negfeats = [(word_feats(nltk.corpus.movie_reviews.words(fileids=[f])), 'neg') for f in negids]
        posfeats = [(word_feats(nltk.corpus.movie_reviews.words(fileids=[f])), 'pos') for f in posids]
     
        negcutoff = len(negfeats)*3/4
        poscutoff = len(posfeats)*3/4
     
        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
     
        classifier = nltk.NaiveBayesClassifier.train(trainfeats)

        sentiment_file = open('.sentiment_classifier', 'wb')
        # use the more efficient binary format
        pickle.dump(classifier, sentiment_file, 1)
        sentiment_file.close()

    return classifier.classify(words)

def tag_pos(textfile):
    words = get_words(textfile)
    try:
        tagger_file = open('.pos_tagger', 'rb')
        tagger = pickle.load(tagger_file)
        tagger_file.close()
    except:
        # use the brown corpus to create a ~90% accurate part-of-speech tagger
        print "generating part-of-speech tagger..."

        brown_sents = nltk.corpus.brown.tagged_sents()
        size = int(0.9 * len(brown_sents))

        train_sents = brown_sents[:size]

        t0 = nltk.DefaultTagger('NN')
        t1 = nltk.UnigramTagger(train_sents, backoff=t0)
        t2 = nltk.BigramTagger(train_sents, backoff=t1)
        tagger = nltk.TrigramTagger(train_sents, backoff=t2)

        tagger_file = open('.pos_tagger', 'wb')
        pickle.dump(tagger, tagger_file, -1)
        tagger_file.close()

    return tagger.tag(words)

def analyze(textfile):
    corpus = get_corpus()
    analysis = {}
    analysis['word_count'] = word_count(textfile)
    analysis['histogram'] = histogram(textfile)
    analysis['sentiment'] = classify_sentiment(textfile)
    analysis['pos'] = tag_pos(textfile)
    return analysis

if __name__ == "__main__":
    import sys
    for textfile in sys.argv[1:]:
        print analyze(textfile)
