from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
import spacy
import numpy as np


#Tokenization, Stop words, punctuation and numerical string removal, and lemmatization
class Preprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        #might need to run "python -m spacy download en_core_web_sm"
        self.preprocessor = spacy.load('en_core_web_sm')
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        preprocessed = np.array([self.__preprocess(x) for x in X])
        return preprocessed
    
    def __preprocess(self, news_headline):
        tokens = [t.lemma_ for t in self.preprocessor(news_headline) if not t.is_punct and not t.is_stop and not t.is_digit]
        tokens = [token for token in tokens if not(token in ['-', '|'])]
        return ' '.join(tokens)