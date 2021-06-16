import string
import os
import numpy as np
import pickle
from joblib import dump,load
import spacy

nlp1 = spacy.load('en_core_web_sm')
nlp2 = spacy.load('en_core_web_sm')

classifier_absolute_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'binary_classifier.pkl')
preprocessor_absolute_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'preprocessor.pkl')

def pre_process(newString):
    newString = newString.replace("-"," ")
    newString = newString.replace("'s","")
    return newString.lower()


def rep_entity(s):
    doc = s
    newString = str(s)
    for e in reversed(doc.ents): #reversed to not modify the offsets of other entities when substituting
        label = e.label_
        if label in ["ORG","PERSON","EVENT","PRODUCT", "GPE", "LOC"]:
            continue

        start = e.start_char
        end = start + len(e.text)
        newString = newString[:start] + label + newString[end:]

    newString = newString.strip()
    newString = newString.translate(str.maketrans(dict.fromkeys(string.punctuation + "\n\t’:")))
    return newString


def post_process(s):
    doc = s
    tokens = [word.lemma_ for word in doc if not word.is_stop]
    text = " ".join(tokens)
    return text 


def test_sent(s):
    s = pre_process(s)
    s = nlp1(s)
    s = rep_entity(s)
    s = nlp2(s)
    s = post_process(s)
    return s


def predict(test_reviews):
    with open(classifier_absolute_path,"rb") as pkl_obj:
        classifier = pickle.load(pkl_obj)
    
    with open(preprocessor_absolute_path,"rb") as pkl_obj:
        cv = pickle.load(pkl_obj)

    if isinstance(test_reviews,str):
        test_review = test_reviews
        test_review = test_sent(test_review)
        test_input_array = cv.transform([test_review]).toarray()
        test_input_array = np.transpose(test_input_array)
        test_input_array = test_input_array[:,0]
        res = classifier.predict([test_input_array])
        return res[0]
    elif isinstance(test_reviews,list):
        result=[]
        for test_review in test_reviews:
            test_review = test_sent(test_review)
            test_input_array = cv.transform([test_review]).toarray()
            test_input_array = np.transpose(test_input_array)
            test_input_array = test_input_array[:,0]
            res = classifier.predict([test_input_array])
            result.append(res[0])
        return result
    print('Please provide a string or a list.')


# test = ["5 man died at airplane crash yestarday","4 people went to justin bieber concert"]

# test_df = pd.read_csv("all-news.csv").sample(1000)


