#!/usr/bin/env python
# coding: utf-8

# # Module 5: Natural Language Processing
# ## Lecture 3: Text Classification

# * Classification is a topic in machine learning.
# * Classification is supervised, meaning you need to provide correct classification labels.
# * Data should be partitioned into training and test data.
# * There are many classification models, but only naive Bayes will be used in this lecture.
# * More details about machine learning will be covered in the next module.

# # References for This Lecture
# * NLTK Book, Ch. 6
#     * http://www.nltk.org/book/ch06.html
#     * Sections 1.1, 1.3, 1.4, 2.1

# # Gender Classification

# In[1]:


# names can be clasified into male and female names
# what features should be used?
# let's start with the last letter of the name
def gender_features(word):
    return {'last_letter': word[-1]}

gender_features('John')


# In[4]:


# NLTK contains lists of male and female names
# load and shuffle them
import nltk
from nltk.corpus import names
import random

labeled_names = ([(name, 'male') for name in names.words('male.txt')] + 
                 [(name, 'female') for name in names.words('female.txt')])
random.shuffle(labeled_names)
labeled_names[:10]


# In[6]:


# it's necessary to partition the data into
# training and test data
# use the training data to train a naive Bayes classifier
# and evaluate the classifier on the test data
featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)


# In[1]:


# you can apply the classifier to a particular name as well
# it correctly classifies my name!
classifier.classify(gender_features('Jim'))


# In[13]:


# you can also examine which feature values were most useful
# likelihood ratios are displayed
classifier.show_most_informative_features(5)


# # Document Classification

# In[11]:


# it's possible to classify documents into categories
# let's classify the first nursing note of each ICU stay
# according to ICU mortality
# here is the SQL query
from nltk.corpus import movie_reviews
documents = [(list(movie_reviews.words(fileid)), category)
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)


# In[13]:


# run the query and extract data from MIMIC
documents[0]


# In[29]:


# again, the most difficult step is feature extraction
# let's use the presence of the 1000 most common words
import re

movie_tokens = []
for (review, rating) in documents:
    movie_tokens += review

# apply raw text processing we studied in lecture 1
movie_tokens = [nltk.PorterStemmer().stem(token) for token in movie_tokens 
             if len(token) > 1 and
             not re.search(r'^\*\*.+$', token) and 
             not re.search(r'^.+\*\*$', token) and                 
             not re.search(r'^[0-9]+', token)]    
    
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words.keys())[:2000]
word_features[:20]


# In[30]:


# feature extractor
def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


# In[39]:


# train a naive Bayes classifier and evaluate it on test data
featuresets = [(document_features(review), rating) for (review, rating) in documents]
train_set, test_set = featuresets[:200], featuresets[200:]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)


# In[40]:


# most important features
classifier.show_most_informative_features(5)


# # POS Tagging with Classification

# In[41]:


# instead of manually creating a POS tagger
# it's possible to train a classifier to learn suffix patterns
# let's extract common suffixes first
from nltk.corpus import brown

suffix_fdist = nltk.FreqDist()
for word in brown.words():
    word = word.lower()
    suffix_fdist[word[-1:]] += 1
    suffix_fdist[word[-2:]] += 1
    suffix_fdist[word[-3:]] += 1

common_suffixes = [suffix for (suffix, count) in suffix_fdist.most_common(100)]
common_suffixes[:10]


# In[42]:


# define a feature extractor
# that indicates whether the given word ends with 
# one of the common suffixes
def pos_features(word):
    features = {}
    for suffix in common_suffixes:
        features['endswith({})'.format(suffix)] = word.lower().endswith(suffix)
    return features


# In[43]:


# train a naive Bayes classifier and evaluate
tagged_words = brown.tagged_words(categories='news')
featuresets = [(pos_features(n), g) for (n,g) in tagged_words]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)


# In[36]:


# see how the classifier performs for a specific word
classifier.classify(pos_features('health'))


# # Sentence Segmentation with Classification

# In[21]:


# setence segmentation essentially looks for 
# sentence-ending punctuation
# which can be learned using machine learning
# first we need segmented data
import nltk
sents = nltk.corpus.treebank_raw.sents()
tokens = []
boundaries = set()
offset = 0
for sent in sents:
    tokens.extend(sent)
    offset += len(sent)
    boundaries.add(offset-1)


# In[22]:


# tokens contains tokens from individual sentences
tokens[:10]


# In[35]:


# boundaries contains indexes of sentence-boundary tokens
print boundaries


# In[31]:


# extract the following features
def punct_features(tokens, i):
    return {'next-word-capitalized': tokens[i+1][0].isupper(),
            'prev-word': tokens[i-1].lower(),
            'punct': tokens[i],
            'prev-word-is-one-char': len(tokens[i-1]) == 1}


# In[32]:


# extract features and use them 
# to train and evaluate a naive Bayes classifier
featuresets = [(punct_features(tokens, i), (i in boundaries))
               for i in range(1, len(tokens)-1)
               if tokens[i] in '.?!']
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)


# # Module 5 Closing Remarks
# * There is a lot more to NLP
#     * Such as analyzing sentence structure, grammar, etc
#     * If interested, read the rest of the NLTK book
# * This lecture is a nice segue to Module 6 on machine learning
# * This module was important for the course project
