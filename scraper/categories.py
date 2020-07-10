import pickle, os

CATEGORIES = {
    'b': 'Business',
    't': 'Science and Technology',
    'e': 'Entertainment',
    'm': 'Health'
}

def predict(title: str):
    path = os.path.join(os.path.dirname(__file__), 'model')
    
    filename = 'finalized_model.pkl'
    vect = 'vectorizer.pkl'
    enc = 'encoder.pkl'

    model = pickle.load(open(os.path.join(path, filename), 'rb'))
    vectorizer = pickle.load(open(os.path.join(path, vect), 'rb'))
    encoder = pickle.load(open(os.path.join(path, enc), 'rb'))
    result = model.predict(vectorizer.transform([title]))

    return CATEGORIES[encoder.inverse_transform(result)[0]]
