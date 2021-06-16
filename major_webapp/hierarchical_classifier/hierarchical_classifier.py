import pandas as pd
import spacy
import pickle

from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from sklearn_hierarchical_classification.classifier import HierarchicalClassifier
from hierarchical_classifier.modelling_utils import Preprocessor

def predict(json_array):
    with open("./hierarchical_classifier/pickled_objects/hierarchy_classifier.pkl","rb") as pkl_obj:
        model = pickle.load(pkl_obj)

    text_preprocessor = Preprocessor()
    df = pd.DataFrame.from_dict(json_array)
    dtm = text_preprocessor.fit_transform(df.title)
    df["result"] = model.predict(dtm)
    return df

# if __name__ == "__main__":
#     test_data = [
#             {"id" : "1" ,"title" : "Joe Biden wins election 2020"},
#             {"id" : "2" ,"title" : "Many people are in threats due to hurricane"}
#         ]
    
#     predict(test_data)
