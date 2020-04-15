import pickle
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json
import sys
from sklearn.neighbors import KNeighborsClassifier
import cleaning
from sklearn.model_selection import KFold
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def tweet_cleaner(tweet):  
  stop_words = set(stopwords.words('indonesian'))

  dictionary = np.array([word.replace('\n', '') for word in open("E:/myproject/SKRIPSI/data/kata-dasar.txt", 'r').readlines()])

  # stopword tambahan
  stop = ['tp','kl','yg','klo','tpi','yang', 'untuk', 'pada', 'ke', 'para', 'namun', 'menurut', 'antara', 'dia', 'dua', 'ia', 'seperti', 'jika', 'jika', 'sehingga', 'kembali', 'dan', 'tidak', 'ini', 'karena',  'kepada', 'oleh', 'saat', 'harus', 'sementara', 'setelah', 'belum', 'kami', 'sekitar', 'bagi', 'serta', 'di', 'dari', 'telah', 'sebagai', 'masih', 'hal', 'ketika', 'adalah', 'itu', 'dalam', 'bisa', 'bahwa', 'atau', 'hanya', 'kita', 'dengan', 'akan', 'juga', 'ada', 'mereka', 'sudah', 'saya', 'terhadap', 'secara', 'agar', 'lain', 'anda', 'begitu', 'mengapa', 'kenapa', 'yaitu', 'yakni', 'daripada', 'itulah', 'lagi', 'maka', 'tentang', 'demi', 'dimana', 'kemana', 'pula', 'sambil', 'sebelum', 'sesudah', 'supaya', 'guna', 'kah', 'pun', 'sampai', 'sedangkan', 'selagi', 'sementara', 'tetapi', 'apakah', 'kecuali', 'sebab', 'selain', 'seolah', 'seraya', 'seterusnya', 'tanpa', 'agak', 'boleh', 'dapat', 'dsb', 'dst', 'dll', 'dahulu', 'dulunya', 'anu', 'demikian', 'tapi', 'ingin', 'juga', 'nggak', 'mari', 'nanti', 'melainkan', 'oh', 'ok', 'seharusnya', 'sebetulnya',  'setiap', 'setidaknya', 'sesuatu', 'pasti', 'saja', 'toh', 'ya', 'walau', 'tolong', 'tentu', 'amat', 'apalagi', 'bagaimanapun']
  # seleksi stopword yang belum ada pada list stop_words bawaan nltk
  stop_add = [x for x in stop if x not in stop_words]
  for word in stop_add:
    stop_words.add(word)

  factory = StemmerFactory()
  stemmer = factory.create_stemmer()

  clean_tokens = np.array([])
  lower = tweet.lower()
  no_number = re.sub(r'\d+', '', lower)
  no_url = re.sub(r"http\S+", "", no_number)
  no_dash = no_url.replace("-", " ")
  no_punctuation = no_dash.translate(str.maketrans('', '', string.punctuation))
  no_white_space = re.sub(' +', ' ', no_punctuation)
  tokens = word_tokenize(no_white_space)

  for token in tokens:
    if token in dictionary or token in stop_words:    
      clean_tokens = np.append(clean_tokens, token)
    else:    
      stem_token = stemmer.stem(token)
      clean_tokens = np.append(clean_tokens, stem_token)

  # remove stopwords
  no_stopwords = [i for i in clean_tokens if not i in stop_words and i in dictionary]
  
  stem = stemmer.stem(' '.join(no_stopwords))
  result = re.sub(r'\d+', '', ''.join(stem))
  result = re.sub(' +', ' ', result)
  return result

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def stemming(data):
  print('stemming...')
  progress(0, len(data), status='Preparing...')
  output_text = []
  for item in data.text.to_list():
    clean_tweet = tweet_cleaner(item)
    output_text.append(clean_tweet)
    progress(len(output_text), len(data), status=f'Successfully stem {len(output_text)} of {len(data)}')

  return output_text


def tfidf(data, new_data):  
  print("preprocessing...")
  
  # # preprocessing
  # output_text = []
  # for item in data.text.to_list():
  #   clean_tweet = tweet_cleaner(item)
  #   output_text.append(clean_tweet)
    
  data['stem_text'] = stemming(data)
  new_data['stem_text'] = stemming(new_data)

  print("tf-idf...")
  tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1,2))
  feature = tfidf.fit_transform(data['stem_text']).toarray()
  new_feature = tfidf.transform(new_data['stem_text']).toarray()

  return new_feature

def retrain_tfidf(data):
  print("preprocessing...")
    
  data['stem_text'] = stemming(data)  

  print("tf-idf...")
  tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1,2))
  feature = tfidf.fit_transform(data['stem_text']).toarray()  

  return feature

def predict_from_crawling():
  print('predict fromcrawling...')
  train_data = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')
  crawl_data = pd.read_csv('E:/myproject/SKRIPSI/data/data-crawl.csv')

  predict_data = crawl_data[crawl_data.label == 0]

  feature = tfidf(train_data, predict_data)
  train_data = train_data.drop('stem_text', axis=1)
  predict_data = predict_data.drop('stem_text', axis=1)

  knn = pickle.load(open('E:/myproject/SKRIPSI/model/model.pkl', 'rb'))
  print('predicting...')
  pred = knn.predict(feature)

  crawl_data.iloc[-len(predict_data):, -1:] = pred

  print('done...')
  
  print('saving new predicted data...')

  crawl_data.to_csv('E:/myproject/SKRIPSI/data/data-crawl.csv', index=False, header=True)
  print(crawl_data.tail())

  return "predict done.. refresh page to update maps"

def retrain_model():
  train_data = pd.read_csv('E:/myproject/SKRIPSI/data/data-kombinasi-terbaik.csv')

  feature = retrain_tfidf(train_data)
  train_data = train_data.drop('stem_text', axis=1)

  X = feature
  y = train_data['label']
  kf = KFold(n_splits=10)
  split = list(kf.split(X))
  # split[0][1] -> data testing, sisanya data training
  # di case ini, karena data testing sudah diketahui indexnya 1-120 saja,
  # maka data training bisa dipastikan indexnya mulai 121-akhir

  X_test = X[:121]
  y_test = y[:121]
  X_train = X[121:]
  y_train = y[121:]
  # selanjutnya variabel training diatas di fit ke model knn
  # kemudian model knn yang baru di update disimpan

  # knn = pickle.load(open('E:/myproject/SKRIPSI/model/model.pkl', 'rb'))
  knn = KNeighborsClassifier(n_neighbors=28, metric='cosine')
  knn.fit(X_train, y_train)

  y_pred = knn.predict(X_test)
  metrics_acc = metrics.accuracy_score(y_test, y_pred)

  # save model
  pickle.dump(knn, open('E:/myproject/SKRIPSI/model/model.pkl', 'wb'))
  print(metrics_acc)

  from sklearn.metrics import confusion_matrix
  import seaborn as sns
  import matplotlib.pyplot as plt
  import datetime

  date = datetime.datetime.today()

  fig, ax = plt.subplots(figsize=(8,8))
  # category = dataset[['nama_label', 'label fix']].drop_duplicates().sort_values('label fix')
  category = ['positif', 'negatif', 'netral']
  conf_matrix = confusion_matrix(y_test, y_pred)
  sns.heatmap(conf_matrix, annot=True, fmt='d', xticklabels=category, yticklabels=category)
  plt.xlabel('Predicted')
  plt.ylabel('Actual')
  # plt.show()
  fig.savefig('E:/myproject/SKRIPSI/plots/conf-matrix-{}.png'.format(date.strftime('%Y-%m-%d')))

  return str(metrics_acc)