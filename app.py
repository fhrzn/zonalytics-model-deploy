from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import prediction as clf
import timeit

app = Flask(__name__)

CORS(app)

@app.route('/')
def home():
    # return render_template('index.html')
    return 'HELLO WORLD'

@app.route('/api/predict', methods=['POST'])
def coba_predict():

    text = request.get_json()['tweets']        
    predict = clf.predict(text)
    return jsonify({"predict": predict, "elapsed_time": timeit.timeit(predict)})

if __name__ == '__main__':
    app.run(debug=True)