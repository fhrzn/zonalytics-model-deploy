import pandas as pd
import json

def allData():
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-predicted.csv')
    return json.loads(df.to_json(orient='records'))

def dataByProvince(prov):    
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-predicted.csv')
    df = df[df.provinsi == prov]
    return json.loads(df.to_json(orient='records'))

def getListProvince():
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-predicted.csv')
    listdf = df.provinsi.unique().tolist()
    listdf.sort()
    return listdf

def allSentiment():
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-predicted.csv')
    labels = df.groupby('label').label.count()
    return json.loads(labels.to_json(orient='records'))

def sentimentByProv(prov):
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-predicted.csv')
    df = df[df.provinsi==prov]
    labels = df.groupby('label').label.count()
    return json.loads(labels.to_json(orient='index'))