#!/usr/bin/env python
# text analysis module
from collections import defaultdict
import random
import re
import subprocess
import cPickle as pickle

import nltk
from nltk.corpus import wordnet as wn

def get_similar(word):
    similar = []
    synsets = wn.synsets(word)
    for synset in synsets:
        similar_tos = synset.similar_tos()
        for ss in similar_tos:
            for lemma in ss.lemmas:
                similar.append(lemma.name)

    return similar

def document_features(document):
    try:
        word_features_file = open('.word_features', 'rb')
        word_features = pickle.load(word_features_file)
        word_features_file.close()
    except:
        all_words = nltk.FreqDist(w.lower() for w in nltk.corpus.movie_reviews.words())
        word_features = all_words.keys()[:2000]
        word_features_file = open('.word_features', 'wb')
        pickle.dump(word_features, word_features_file, -1)
        word_features_file.close()

    document_words = set(document)
    features = {}
    for word in word_features:
        if word in document_words:
            features['contains(%s)' % word] = True
            continue
        for similar in get_similar(word):
            if similar in document_words:
                features['contains(%s)' % word] = True

    return features

def get_corpus(path=None):
    if path is None:
        try:
            from sevenfifty import SevenFiftyWords
            sevenfiftywords = SevenFiftyWords()
            path = sevenfiftywords.output_dir
        except:
            return
    return nltk.corpus.PlaintextCorpusReader(path, '.*')

def classify_sentiment(tokens):
    words = document_features(tokens)
    try:
        sentiment_file = open('.sentiment_classifier', 'rb')
        classifier = pickle.load(sentiment_file)
        sentiment_file.close()
    except:
        print "generating sentiment classifier..."
        documents = [(list(nltk.corpus.movie_reviews.words(fileid)), category)
                 for category in nltk.corpus.movie_reviews.categories()
                 for fileid in nltk.corpus.movie_reviews.fileids(category)]
        random.shuffle(documents)
       
        featuresets = [(document_features(d), c) for (d,c) in documents]
        classifier = nltk.NaiveBayesClassifier.train(featuresets)

        sentiment_file = open('.sentiment_classifier', 'wb')
        # use the more efficient binary format
        pickle.dump(classifier, sentiment_file, 1)
        sentiment_file.close()

    return classifier.classify(words)

def tag_pos(tokens):
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

    for sentence in tokens:
        yield tagger.tag(sentence)

def word_count(document):
    """returns the number of words in document"""
    textfile = open(document)
    # normalize whitespace
    raw = ' '.join(line.strip() for line in textfile)
    tokens = nltk.wordpunct_tokenize(raw)
    words = [token.lower() for token in tokens if token.isalpha()]
    return len(words)

def analyze(document):
    textfile = open(document)
    # normalize whitespace
    raw = ' '.join(line.strip() for line in textfile)
    tokens = nltk.wordpunct_tokenize(raw)
    sentences = [nltk.word_tokenize(sentence) for sentence in nltk.sent_tokenize(raw)]
    words = [token.lower() for token in tokens if token.isalpha()]

    important_words = [word for word in words if word not in nltk.corpus.stopwords.words('english')]
    analysis = {}

    word_count = len(words)
    vocab = sorted(set(words))

    fdist = nltk.FreqDist(important_words)

    lexical_diversity = float(word_count) / len(vocab)

    sentence_count = len(sentences)

    analysis['word_count'] = word_count
    analysis['sentence_count'] = sentence_count
    analysis['vocab'] = fdist
    analysis['sentiment'] = classify_sentiment(words)
    analysis['parts-of-speech'] = list(tag_pos(sentences))
    return analysis

if __name__ == "__main__":
    import sys
    print get_similar(sys.argv[1])
