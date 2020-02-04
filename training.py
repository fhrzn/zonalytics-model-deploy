print('start training...')

"""# Load Data"""

import pandas as pd

def load_data():
    print("loading dataset...")
    df = pd.read_csv('E:/myproject/SKRIPSI/data/data-dummy.csv')
    return df

def set_label(row_number, assigned_value):  
  return assigned_value[row_number]

dummy = load_data()
label_name = {1: 'positif', 2: 'negatif', 3: 'netral'}
dummy['nama_label'] = dummy['label'].apply(set_label, args=(label_name, ))


"""# Preprocessing"""

import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import numpy as np

print('preprocessing...')

# nltk.download('punkt')
# nltk.download('stopwords')
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

def tweet_cleaner(tweet):
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

origin_text = dummy.text.to_list()
output_text = []

for i, item in enumerate(origin_text):
  clean_tweet = tweet_cleaner(item)
  output_text.append(clean_tweet)

dummy['stem_text'] = output_text

"""# TF-IDF"""

from sklearn.feature_extraction.text import TfidfVectorizer

print('tf-idf process...')
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1,2))
feature = tfidf.fit_transform(dummy['stem_text']).toarray()   # ini yang dipakai buat klasifikasi
labels = dummy['label']

"""# Classification"""

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import math

print('splitting data...')
x = feature
y = dummy['label']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=0) 

total_n = int(math.floor(math.sqrt(len(dummy))))

"""# Tuning Hyperparameter """
"""### Tuning manual"""

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

print('Tuning hyperparameter...')
kf = KFold(n_splits=10)
k_range = range(1,total_n+1)
k_score = []
i=1
y_test_reindex = y_test.reset_index(drop=True)

for k in k_range:
  knn = KNeighborsClassifier(n_neighbors=k, metric='cosine')
  knn.fit(X_train, y_train)
  scores = []
  for _, test_index in kf.split(X_test):  
    test_data = X_test[test_index]  
    test_label = y_test_reindex[test_index]    
    pred_label = knn.predict(test_data)  
    scores.append(metrics.accuracy_score(test_label, pred_label))        
    
  k_score.append(np.mean(scores))

# hasil tuning hyperparameter K terbaik
best_k = int(np.where(k_score==np.amax(k_score))[0]+1)
print('K terbaik: ',best_k)


"""# Save model to Pickle """

import pickle

print('X_test: ', X_test.shape)

print('testing...')
knn = KNeighborsClassifier(n_neighbors=best_k, metric='cosine')
knn.fit(X_train, y_train)
print('Akurasi model: ',knn.score(X_test, y_test))
pickle.dump(knn, open('E:/myproject/SKRIPSI/data/model.pkl', 'wb'))
print('saved model to E:/myproject/SKRIPSI/model/model.pkl')