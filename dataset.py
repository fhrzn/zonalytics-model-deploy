import pandas as pd
import json
import GetOldTweets3 as got
from TwitterAPI import TwitterAPI
from datetime import datetime
import cleaning
import prediction
import sys
import csv
from io import StringIO

def allData():
    df = pd.read_csv('./data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('./data/data-crawl.csv')
    df = pd.concat([df, crawl]).reset_index(drop=True)
    return json.loads(df.to_json(orient='records'))

def dataByProvince(prov):    
    df = pd.read_csv('./data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('./data/data-crawl.csv')
    df = pd.concat([df, crawl]).reset_index(drop=True)
    df = df[df.provinsi == prov]
    return json.loads(df.to_json(orient='records'))

def getListProvince():
    df = pd.read_csv('./data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('./data/data-crawl.csv')
    df = pd.concat([df, crawl]).reset_index(drop=True)
    listdf = df.provinsi.unique().tolist()
    listdf.sort()
    return listdf

def allSentiment():
    df = pd.read_csv('./data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('./data/data-crawl.csv')
    df = pd.concat([df, crawl]).reset_index(drop=True)
    labels = df.groupby('label').label.count()
    # return json.loads(labels.to_json(orient='records'))
    return json.loads(json.dumps({
        'data': json.loads(labels.to_json(orient='records')),
        'length': str(len(df))
    }))

def sentimentByProv(prov):
    df = pd.read_csv('./data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('./data/data-crawl.csv')
    df = pd.concat([df, crawl]).reset_index(drop=True)
    df = df[df.provinsi==prov]
    labels = df.groupby('label').label.count()
    # return json.loads(labels.to_json(orient='index'))
    return json.loads(json.dumps({
        'data': json.loads(labels.to_json(orient='index')),
        'length': str(len(df))
    }))

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def crawlData(**kwargs):
    print('crawl data...')
    df = pd.read_csv('./data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('./data/data-crawl.csv')
    df_concat = pd.concat([df, crawl])

    api = TwitterAPI('OOheRS0hK5FQaj6iL75XTILke', 'aDeZ9i3dZ18KjtDiEcNf683hwjKC4MLyAR3v1f1FqHiW3QdNEz', '831073699411275776-7HDtuctKY7orzuEIRPhEkChTgo2JJ5n', 'txslgzywJrEMmy6zi2e8AdpikcqsWo6k9hueSJMibSeZx')
    # api = TwitterAPI('jToPvkoi8cePreVNCwWsn0Xnz', 'V7N9XSmU3lfNyKurDsje9vxo6wM6GZIcpJnAjUYmkVglhIaqZg', '1088104775588012032-W9v2m9OoD9ToXrBonS45iBVzkiocLK', 'UWN3V01IbXZIKWbSZGD4o6hYpOXLMmyATV3H42W8gT1nJ')

    start_date = kwargs.get('start_date', None)
    end_date = kwargs.get('end_date', None)    
    keyword = kwargs.get('keyword',None)


    # scraping process
    if start_date != None and end_date != None and keyword != None:
        print(keyword, start_date, end_date)
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setSince(start_date).setUntil(end_date)
    else:
        date = df_concat['date'].sort_values(ascending=False).iloc[0]
        print(date)

        today = datetime.today().strftime('%Y-%m-%d')    
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch('zonasi sekolah').setSince(date).setUntil(today)

    print(tweetCriteria)
    # tweetCriteria = got.manager.TweetCriteria().setQuerySearch('zonasi sekolah').setSince('2018-11-01').setUntil('2018-12-31')
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    print('scraping start')
    total = len(tweets)
    print('writing %d tweets...' % total)

    tw_list = []    
    for tweet in tweets :
        progress(len(tw_list), len(tweets), status=f'Successfully write {len(tw_list)} of {len(tweets)}')
        text = tweet.text
        username = '@'+tweet.username
        date = tweet.date.date()
        time = tweet.date.time()
        tweetID = int(tweet.id)

        # Request API for getting user's location
        req = api.request('statuses/show/:%d' % tweetID)

        if req.status_code != 200:
            lokasi = ''
            status_code = req.status_code
        else :
            status_code = 200
            for item in req.get_iterator():
                # lokasi
                if item['user']['location'] != None:
                    lokasi = item['user']['location'].replace(',','').replace('\n', '')

        # save tweet to dictionary
        tweet_dict = {
            'date': date,
            'lokasi': lokasi,
            'status': status_code,
            'text': text,
            'time': time,
            'tweet_id': tweetID,
            'username': username,
        }

        tw_list.append(tweet_dict)

    if len(tw_list) <= 0:
        return 'no new data'

    df = pd.DataFrame(tw_list)    
    
    data = cleaning.clean(df)
    print("data", len(data))
    data['label'] = 0    
    old_data = pd.read_csv('./data/data-crawl.csv')    

    if len(old_data) > 0:        
        same = data['text'].isin(old_data['text'])
        data.drop(data[same].index, inplace=True)        

    if len(data) <= 0:
        return 'no new data'

    old_data = old_data.append(data, ignore_index = True)        
    old_data.to_csv('./data/data-crawl.csv', index=False, header=True)
    
    return prediction.predict_from_crawling()

def getPredictedData():
    crawl = pd.read_csv('./data/data-crawl.csv')
    crawl['tweet_id'] = crawl['tweet_id'].apply(str)
    predict = crawl[crawl.label!=0]
    # remove unused column
    # predict = predict.drop(['lokasi', 'status', 'tweet_id', 'username'], axis=1)
    # reorder column
    # cols = ['text', 'date', 'time', 'provinsi', 'label']
    # predict = predict.reindex(columns=cols)
    return json.loads(predict.to_json(orient='records'))

def getTrainingData():
    training = pd.read_csv('./data/data-kombinasi-terbaik.csv')
    training['tweet_id'] = training['tweet_id'].apply(str)
    training['label'] = training['label'].apply(int)
    predict = training[training.label!=0]
    # remove unused column
    # predict = predict.drop(['lokasi', 'status', 'tweet_id', 'username'], axis=1)
    # reorder column
    # cols = ['text', 'date', 'time', 'provinsi', 'label']
    # predict = predict.reindex(columns=cols)
    return json.loads(predict.to_json(orient='records'))

def allSentimentByYear():
    data = pd.read_csv('./data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('./data/data-crawl.csv')

    predict = pd.concat([data, crawl], sort=False)
    predict = predict[predict.label!=0]
    predict['date'] = predict['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    predict = predict.groupby([predict['date'].map(lambda x: x.year), 'label']).label.size()
    
    buffer = StringIO()
    predict.to_csv(buffer, header=False)
    buffer.seek(0)

    tahun = 0
    positif = 0
    negatif = 0
    netral = 0

    listTahun = []
    listPositif = []
    listNegatif = []
    listNetral = []
        
    for row in csv.reader(buffer):
        currentYear = row[0]        

        if tahun==0:
            tahun = currentYear
        if tahun!=currentYear:
            
            listTahun.append(tahun)
            listPositif.append(positif)
            listNegatif.append(negatif)
            listNetral.append(netral)

            tahun = currentYear
            positif = 0
            negatif = 0
            netral = 0
        
        if row[1] == '1':
            positif = str(row[2])
        elif row[1] == '2':
            negatif = str(row[2])
        elif row[1] == '3':
            netral = str(row[2])

    listTahun.append(tahun)
    listPositif.append(positif)
    listNegatif.append(negatif)
    listNetral.append(netral)

    return json.loads(json.dumps({
        'positif': listPositif,
        'negatif': listNegatif,
        'netral': listNetral,
        'tahun': listTahun
    }))

def sentimentByYearByProv(prov):
    data = pd.read_csv('./data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('./data/data-crawl.csv')

    predict = pd.concat([data, crawl], sort=False)
    predict = predict[predict.provinsi == prov]
    predict = predict[predict.label!=0]
    predict['date'] = predict['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    predict = predict.groupby([predict['date'].map(lambda x: x.year), 'label']).label.size()

    buffer = StringIO()
    predict.to_csv(buffer, header=False)
    buffer.seek(0)

    tahun = 0
    positif = 0
    negatif = 0
    netral = 0
    
    listTahun = []
    listPositif = []
    listNegatif = []
    listNetral = []
        
    for row in csv.reader(buffer):
        currentYear = row[0]

        if tahun==0:
            tahun = currentYear
        if tahun!=currentYear:

            listTahun.append(tahun)
            listPositif.append(positif)
            listNegatif.append(negatif)
            listNetral.append(netral)

            tahun = currentYear
            positif = 0
            negatif = 0
            netral = 0
        
        if row[1] == '1':
            positif = str(row[2])
        elif row[1] == '2':
            negatif = str(row[2])
        elif row[1] == '3':
            netral = str(row[2])

    listTahun.append(tahun)
    listPositif.append(positif)
    listNegatif.append(negatif)
    listNetral.append(netral)

    return json.loads(json.dumps({
        'positif': listPositif,
        'negatif': listNegatif,
        'netral': listNetral,
        'tahun': listTahun
    }))

def addTrainingData(data):
    tweet = {
        'tweet_id': data['tweet_id'],
        'text': data['text'],
        'username': data['username'],
        'date': data['date'],
        'time': data['time'],
        'lokasi': data['lokasi'],
        'status': data['status'],
        'provinsi': data['provinsi'],
        'label': data['label'],
    }    

    # print(tweet['tweet_id'])
    
    training = pd.read_csv('./data/data-kombinasi-terbaik.csv')    
    train_df = training.append(tweet, ignore_index=True)
    train_df['label'] = train_df['label'].apply(int)
    train_df.to_csv('./data/data-kombinasi-terbaik.csv', index=None, header=True)

    crawl = pd.read_csv('./data/data-crawl.csv')
    # crawl_df = crawl[crawl.tweet_id != tweet['tweet_id']]
    crawl_df = crawl.query('tweet_id != {}'.format(tweet['tweet_id']))
    # print(crawl_df.head())
    crawl_df.to_csv('./data/data-crawl.csv', index=None, header=True)

    return 'add training data done.'