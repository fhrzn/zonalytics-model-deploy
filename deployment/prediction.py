import pickle
import preprocess

MODEL_PATH = '../model/model.pkl'
VECTORIZER_PATH = '../model/vectorizer.pkl'
TRANS_LABEL = {
    1: 'positive',
    2: 'negative',
    3: 'neutral'
}

def __load_model():
    model = pickle.load(open(MODEL_PATH, 'rb'))
    vectorizer = pickle.load(open(VECTORIZER_PATH, 'rb'))

    return (model, vectorizer)

def predict(text):
    print(text)
    
    # load saved model and tfidf weight
    model, vectorizer = __load_model()    

    # clean text
    clean_text = preprocess.clean(text)    

    # transform
    trans_text = vectorizer.transform([clean_text])    

    label = model.predict(trans_text).tolist()[0]
    probability = model.predict_proba(trans_text).tolist()[0]    
    

    # prediction
    return {
        'original_text': text,
        'cleaned_text': clean_text,
        'label': TRANS_LABEL[label],
        'positive_probability': probability[0],
        'negative_probability': probability[1],
        'neutral_probability': probability[2]
    }    