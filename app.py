from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pickle
import prediction as clf
import timeit
import dataset
import pandas as pd

app = Flask(__name__, static_url_path='/asset')

CORS(app)

df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
length = len(df)

@app.route('/')
def home():
    # return render_template('index.html')
    return 'HELLO WORLD'

@app.route('/js/geo/<path:path>')
def send_js(path):
    return send_from_directory('asset', path)

@app.route('/api/predict', methods=['POST'])
def coba_predict():

    text = request.get_json()['tweets']        
    predict = clf.predict(text)
    return jsonify({"predict": predict, "elapsed_time": timeit.timeit(predict)})

@app.route('/api/data', methods=['GET'])
def getAllData():
    return jsonify({"data":dataset.allData()})

@app.route('/api/data/<prov>', methods=['GET'])
def getDataByProvince(prov):
    return jsonify({"data":dataset.dataByProvince(prov)})

@app.route('/api/province')
def getListProvince():
    return jsonify({"data":dataset.getListProvince()})

@app.route('/api/sentiment', methods=['GET'])
def getAllSentiment():
    return jsonify({"data":dataset.allSentiment(), "total":length})

@app.route('/api/sentiment/<prov>', methods=['GET'])
def getSentimentByProvince(prov):
    return jsonify({"data":dataset.sentimentByProv(prov), "total":length})

@app.route('/api/fetch-data', methods=['GET'])
def fetchNewData():
    return jsonify({'status':dataset.crawlData()})

@app.route('/api/update-sentiment', methods=['GET'])
def updateSentiment():
    predict = clf.predict_from_crawling()
    return jsonify({'status':predict})

if __name__ == '__main__':
    app.run(debug=True)