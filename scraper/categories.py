import pickle, os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

def predict(title: str):
    path = os.path.join(os.getcwd(), 'app', 'model')
    filename = 'finalized_model.pkl'
    vect = 'vectorizer.pkl'
    enc = 'encoder.pkl'
    model = pickle.load(open(os.path.join(path, filename), 'rb'))
    vectorizer = pickle.load(open(os.path.join(path, vect), 'rb'))
    encoder = pickle.load(open(os.path.join(path, enc), 'rb'))
    result = model.predict(vectorizer.transform([title]))
    return encoder.inverse_transform(result)[0]
