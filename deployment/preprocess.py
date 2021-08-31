import numpy as np
import re
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

stop_words = set(stopwords.words('indonesian'))

dictionary = np.array([word.replace('\n', '') for word in open("../dataset/kata-dasar.txt", 'r').readlines()])

# additional stopword
stop = ['tp','kl','yg','klo','tpi','yang', 'untuk', 'pada', 'ke', 'para', 'namun', 'menurut', 'antara', 'dia', 'dua', 'ia', 'seperti', 'jika', 'jika', 'sehingga', 'kembali', 'dan', 'tidak', 'ini', 'karena',  'kepada', 'oleh', 'saat', 'harus', 'sementara', 'setelah', 'belum', 'kami', 'sekitar', 'bagi', 'serta', 'di', 'dari', 'telah', 'sebagai', 'masih', 'hal', 'ketika', 'adalah', 'itu', 'dalam', 'bisa', 'bahwa', 'atau', 'hanya', 'kita', 'dengan', 'akan', 'juga', 'ada', 'mereka', 'sudah', 'saya', 'terhadap', 'secara', 'agar', 'lain', 'anda', 'begitu', 'mengapa', 'kenapa', 'yaitu', 'yakni', 'daripada', 'itulah', 'lagi', 'maka', 'tentang', 'demi', 'dimana', 'kemana', 'pula', 'sambil', 'sebelum', 'sesudah', 'supaya', 'guna', 'kah', 'pun', 'sampai', 'sedangkan', 'selagi', 'sementara', 'tetapi', 'apakah', 'kecuali', 'sebab', 'selain', 'seolah', 'seraya', 'seterusnya', 'tanpa', 'agak', 'boleh', 'dapat', 'dsb', 'dst', 'dll', 'dahulu', 'dulunya', 'anu', 'demikian', 'tapi', 'ingin', 'juga', 'nggak', 'mari', 'nanti', 'melainkan', 'oh', 'ok', 'seharusnya', 'sebetulnya',  'setiap', 'setidaknya', 'sesuatu', 'pasti', 'saja', 'toh', 'ya', 'walau', 'tolong', 'tentu', 'amat', 'apalagi', 'bagaimanapun']

stop_add = [x for x in stop if x not in stop_words]
for word in stop_add:
  stop_words.add(word)

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def __tweet_cleaner(tweet):
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

def clean(text):
    clean_text = __tweet_cleaner(text)
    return clean_text