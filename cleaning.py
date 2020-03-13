import pandas as pd

from TwitterAPI import TwitterAPI
api = TwitterAPI('OOheRS0hK5FQaj6iL75XTILke', 'aDeZ9i3dZ18KjtDiEcNf683hwjKC4MLyAR3v1f1FqHiW3QdNEz', '831073699411275776-7HDtuctKY7orzuEIRPhEkChTgo2JJ5n', 'txslgzywJrEMmy6zi2e8AdpikcqsWo6k9hueSJMibSeZx')

def rerequest(df):
    # print('rerequest')
    df_r = df[df.status==429]
    tweet_ids = df_r.loc[:, 'tweet_id']
    index = list(range(0, len(tweet_ids)))

    new_lokasi = []
    new_status = []

    for i in range(0, len(tweet_ids)):
        req = api.request('statuses/show/:%d' % tweet_ids.get(i))
        if req.status_code == 429:
            break
        else:
            lokasi = ''
            if req.status_code==200:
                for item in req.get_iterator():
                    if item['user']['location']!=None:
                        lokasi = item['user']['location'].replace(',','')
        
        new_lokasi.append(lokasi)
        new_status.append(req.status_code)
    
    for i in range(0,len(new_lokasi)):
        index = df[df.tweet_id == tweet_ids.get(i)]
        df.loc[index.index, 'lokasi'] = new_lokasi[i]
        df.loc[index.index, 'status'] = new_status[i]

    return df

def data_location(df):
    # print('data location')
    df_lokasi = df[df['lokasi'].isnull() == False]
    return df_lokasi

def remove_duplicate(df):
    # print('remove duplicate')
    df_clean = df.drop_duplicates(subset='text', keep='first')
    return df_clean

def data_city(df):
    # print('data city')
    data_prov = pd.read_csv('E:/myproject/SKRIPSI/data/embedding_kab_kot_prov.csv')
    kota = data_prov.kabupaten_kota.to_list()
    kwstr = '|'.join(map(str.lower, kota))

    df_filter = df[df.lokasi.str.lower().str.contains(kwstr)]
    return df_filter

def mapping_data(df):
    # print('mapping data')
    prov = pd.read_csv('E:/myproject/SKRIPSI/data/embedding_kab_kot_prov.csv')
    kota = prov.kabupaten_kota.to_list()

    map_prov = []
    for i, data in enumerate(df.lokasi.to_list()):
        map_prov.append(find_kota(data, prov, kota))
    
    df.loc[:,('provinsi')] = map_prov
    return df

def find_kota(query, prov, kota):
    # loop dengan index list variabel kota
    for i,item in enumerate(kota):
        # check apakah salah satu nama kota ada di query??
        if item.lower() in query.lower():
            # return nama provinsinya
            return prov.iloc[i][1]  

def clean(df):
    print('clean')
    df_rerequest = rerequest(df)
    # print(df_rerequest.head(), end='\n\n')
    df_location = data_location(df_rerequest)
    # print(df_location.head(), end='\n\n')
    df_duplicate = remove_duplicate(df_location)
    # print(df_duplicate.head(), end='\n\n')
    df_city = data_city(df_duplicate)
    # print(df_city.head(), end='\n\n')
    df_mapping = mapping_data(df_city)

    # print(df_mapping.head())
    return df_mapping
