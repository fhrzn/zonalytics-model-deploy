from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
import flask
import pickle
import prediction as clf
import dataset
import pandas as pd
import os

app = Flask(__name__, static_folder='/asset')

CORS(app)

df = pd.read_csv('./data/data-kombinasi-terbaik.csv')
length = len(df)

@app.route('/')
def home():
    # return render_template('index.html')
    return 'HELLO WORLD'

@app.route('/js/geo/<path:path>')
def send_js(path):
    # root_dir = os.path.dirname(os.getcwd())
    return send_from_directory('./asset', path)
    # return send_from_directory(os.path.join(root_dir, 'asset', 'js'), path)
    
@app.route('/api/data', methods=['GET'])
def getAllData():
    return jsonify({
        "data":dataset.allData()        
    })

@app.route('/api/data/<prov>', methods=['GET'])
def getDataByProvince(prov):
    return jsonify({
        "data":dataset.dataByProvince(prov)        
    })

@app.route('/api/province')
def getListProvince():
    return jsonify({"data":dataset.getListProvince()})

@app.route('/api/sentiment', methods=['GET'])
def getAllSentiment():
    return jsonify({"data":dataset.allSentiment(), "total":length, "series": dataset.allSentimentByYear()})
 
@app.route('/api/sentiment/<prov>', methods=['GET'])
def getSentimentByProvince(prov):
    return jsonify({"data":dataset.sentimentByProv(prov), "total":length, "series": dataset.sentimentByYearByProv(prov)})

@app.route('/api/fetch-data', methods=['GET', 'POST'])
def fetchNewData():
    if flask.request.method == 'POST':        
        data = request.get_json()    
        return jsonify({'status':dataset.crawlData(keyword=data['keyword'], start_date=data['start_date'], end_date=data['end_date'])})
            
    return jsonify({'status':dataset.crawlData()})

@app.route('/api/update-sentiment', methods=['GET'])
def updateSentiment():
    predict = clf.predict_from_crawling()
    return jsonify({'status':predict})

@app.route('/api/predicted-data', methods=['GET'])
def getPredictedData():
    return jsonify({"data": dataset.getPredictedData()})

@app.route('/api/training-data', methods=['GET'])
def getTrainingData():
    return jsonify({"data": dataset.getTrainingData()})

@app.route('/api/sentiment-by-year', methods=['GET'])
def getAllSentimentByYear():
    return dataset.allSentimentByYear()

@app.route('/api/sentiment-by-year/<prov>', methods=['GET'])
def getSentimentByYearByProvince(prov):
    # return jsonify({"data": dataset.sentimentByYearByProv(prov)})
    return dataset.sentimentByYearByProv(prov)

@app.route('/api/add-training-data', methods=['POST'])
def addTrainingData():
    data = request.get_json()
    return jsonify({"data": dataset.addTrainingData(data)})
    # return jsonify({"data": data.tweet_id})

@app.route('/api/retrain-model', methods=['GET'])
def retrainModel():
    return jsonify ({"accuracy": clf.retrain_model()})

if __name__ == '__main__':
    app.run(debug=True)