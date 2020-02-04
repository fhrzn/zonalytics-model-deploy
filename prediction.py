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

def tfidf(data, length_new_data):  
  print("preprocessing...")
  # preprocessing
  output_text = []
  for item in data.text.to_list():
    clean_tweet = tweet_cleaner(item)
    output_text.append(clean_tweet)

  data['stem_text'] = output_text

  print("tf-idf...")
  tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1,2))
  feature = tfidf.fit_transform(data['stem_text']).toarray()

  return feature[-length_new_data:]

def predict(data):    
  print("merging data...")
  # merge data
  old_data = pd.read_csv('E:/myproject/SKRIPSI/data/data-dummy.csv')
  new_data = pd.DataFrame(data)
  # convert NaN ke 0 integer
  new_data['label'] = 0  
  dummy = pd.concat([old_data, new_data]).reset_index(drop=True)  

  feature = tfidf(dummy, len(new_data))
  dummy = dummy.drop('stem_text', axis=1)
  knn = pickle.load(open('E:/myproject/SKRIPSI/model/model.pkl', 'rb'))
  print("predicting...")
  pred = knn.predict(feature)

  dummy.iloc[-len(new_data):, -1:] = pred

  print("done...")

  # save predicted data
  print("saving new predicted data...")
  dummy.to_csv('E:/myproject/SKRIPSI/data/data-predicted.csv', index=False, header=True)
  # print('result: ', pred)
  return json.dumps(pred.tolist())