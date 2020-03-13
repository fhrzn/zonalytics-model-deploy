import pandas as pd
import json
import GetOldTweets3 as got
from TwitterAPI import TwitterAPI
from datetime import datetime
import cleaning

def allData():
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    # dfn = pd.read_csv('E:/myproject/SKRIPSI/data/data-crawl.csv')
    return json.loads(df.to_json(orient='records'))

def dataByProvince(prov):    
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    df = df[df.provinsi == prov]
    return json.loads(df.to_json(orient='records'))

def getListProvince():
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    listdf = df.provinsi.unique().tolist()
    listdf.sort()
    return listdf

def allSentiment():
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    labels = df.groupby('label').label.count()
    return json.loads(labels.to_json(orient='records'))

def sentimentByProv(prov):
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    df = df[df.provinsi==prov]
    labels = df.groupby('label').label.count()
    return json.loads(labels.to_json(orient='index'))

def crawlData():
    print('crawl data...')
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    date = df['date'].sort_values(ascending=False).iloc[0]    

    today = datetime.today().strftime('%Y-%m-%d')

    api = TwitterAPI('OOheRS0hK5FQaj6iL75XTILke', 'aDeZ9i3dZ18KjtDiEcNf683hwjKC4MLyAR3v1f1FqHiW3QdNEz', '831073699411275776-7HDtuctKY7orzuEIRPhEkChTgo2JJ5n', 'txslgzywJrEMmy6zi2e8AdpikcqsWo6k9hueSJMibSeZx')

    # scraping process
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('zonasi sekolah').setSince(date).setUntil(today).setMaxTweets(100)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    print('scraping start')
    total = len(tweets)
    print('writing %d tweets...' % total)

    tw_list = []    
    for tweet in tweets :        
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
                    lokasi = item['user']['location'].replace(',','')

        # save tweet to dictionary
        tweet_dict = {
            'tweet_id': tweetID,
            'text': text,
            'username': username,
            'date': date,
            'time': time,
            'lokasi': lokasi,
            'status': status_code
        }

        tw_list.append(tweet_dict)

    df = pd.DataFrame(tw_list)
    # print(df.head())
    data = cleaning.clean(df)
    data['label'] = 0
    data.to_csv('E:/myproject/SKRIPSI/data/data-crawl.csv', mode='a', index=None, header=True)

    return 'crawling done'