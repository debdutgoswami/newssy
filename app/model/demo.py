import pickle

filename = 'finalized_model.pkl'
vect = 'vectorizer.pkl'
enc = 'encoder.pkl'
model = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open(vect, 'rb'))
encoder = pickle.load(open(enc, 'rb'))
result = model.predict(vectorizer.transform(["buisness is going very well"]))
print(encoder.inverse_transform(result)[0])
