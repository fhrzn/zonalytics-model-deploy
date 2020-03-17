import pandas as pd
import json
import GetOldTweets3 as got
from TwitterAPI import TwitterAPI
from datetime import datetime
import cleaning
import prediction
import sys

def allData():
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('E:/myproject/SKRIPSI/data/data-crawl.csv')
    df = pd.concat([df, crawl]).reset_index(drop=True)
    return json.loads(df.to_json(orient='records'))

def dataByProvince(prov):    
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('E:/myproject/SKRIPSI/data/data-crawl.csv')
    df = pd.concat([df, crawl]).reset_index(drop=True)
    df = df[df.provinsi == prov]
    return json.loads(df.to_json(orient='records'))

def getListProvince():
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('E:/myproject/SKRIPSI/data/data-crawl.csv')
    df = pd.concat([df, crawl]).reset_index(drop=True)
    listdf = df.provinsi.unique().tolist()
    listdf.sort()
    return listdf

def allSentiment():
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('E:/myproject/SKRIPSI/data/data-crawl.csv')
    df = pd.concat([df, crawl]).reset_index(drop=True)
    labels = df.groupby('label').label.count()
    return json.loads(labels.to_json(orient='records'))

def sentimentByProv(prov):
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('E:/myproject/SKRIPSI/data/data-crawl.csv')
    df = pd.concat([df, crawl]).reset_index(drop=True)
    df = df[df.provinsi==prov]
    labels = df.groupby('label').label.count()
    return json.loads(labels.to_json(orient='index'))

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def crawlData():
    print('crawl data...')
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
    crawl = pd.read_csv('E:/myproject/SKRIPSI/data/data-crawl.csv')
    df_concat = pd.concat([df, crawl])
    date = df['date'].sort_values(ascending=False).iloc[0]        
    print(date)

    today = datetime.today().strftime('%Y-%m-%d')

    api = TwitterAPI('OOheRS0hK5FQaj6iL75XTILke', 'aDeZ9i3dZ18KjtDiEcNf683hwjKC4MLyAR3v1f1FqHiW3QdNEz', '831073699411275776-7HDtuctKY7orzuEIRPhEkChTgo2JJ5n', 'txslgzywJrEMmy6zi2e8AdpikcqsWo6k9hueSJMibSeZx')
    # api = TwitterAPI('jToPvkoi8cePreVNCwWsn0Xnz', 'V7N9XSmU3lfNyKurDsje9vxo6wM6GZIcpJnAjUYmkVglhIaqZg', '1088104775588012032-W9v2m9OoD9ToXrBonS45iBVzkiocLK', 'UWN3V01IbXZIKWbSZGD4o6hYpOXLMmyATV3H42W8gT1nJ')

    # scraping process
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('zonasi sekolah').setSince(date).setUntil(today).setMaxTweets(300)
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
                    lokasi = item['user']['location'].replace(',','')

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

    df = pd.DataFrame(tw_list)    
    
    data = cleaning.clean(df)
    data['label'] = 0    
    old_data = pd.read_csv('E:/myproject/SKRIPSI/data/data-crawl.csv')    

    if len(old_data) > 0:        
        same = data['text'].isin(old_data['text'])
        data.drop(data[same].index, inplace=True)        

    if len(data) <= 0:
        return 'no new data'

    old_data = old_data.append(data, ignore_index = True)        
    old_data.to_csv('E:/myproject/SKRIPSI/data/data-crawl.csv', index=False, header=True)
    
    return prediction.predict_from_crawling()