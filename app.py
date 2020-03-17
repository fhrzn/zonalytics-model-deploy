from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
from flask_mysqldb import MySQL
import pickle
import prediction as clf
import timeit
import dataset
import pandas as pd
from settings import MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD
import utils



app = Flask(__name__, static_url_path='/asset')

CORS(app)

app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

db = MySQL(app)

# from blueprint_auth import authentication

df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
length = len(df)

# app.register_blueprint(authentication, url_prefix="/auth")

@app.route('/api/login', methods=['POST'])
def login():
    user_email = request.json['email']
    user_password = request.json['password']
    user_token = utils.validate_user(user_email, user_password)

    if user_token:
        # return jsonify({"jwt_token": user_token})
        return user_token
    else:
        return Response(status=401)

@app.route('/api/register', methods=['POST'])
def register():
    user_email = request.json['email']
    user_password = request.json['password']
    
    if utils.validate_user_input("authentication", email=user_email, password=user_password):
        password_hash = utils.generate_hash(user_password)
        
        if utils.db_write("""INSERT INTO users (email, password) VALUES (%s, %s)""",
                    (user_email, password_hash)):
            return Response(status=201)
        else:
            return Response(status=409)
    else:
        return Response(status=400)

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