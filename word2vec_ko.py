### 네이버 영화리뷰로 한국어 Word2Vec 만들기 ###

import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt
from tqdm import tqdm

# 영화리뷰 데이터 다운로드
# urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings.txt", filename="ratings.txt")

train_data = pd.read_table('ratings.txt')

print(len(train_data)) #리뷰 개수 출력

train_data = train_data.dropna(how='any')   # null 값이 존재하는 행 제거
print(train_data.isnull().values.any())# Null 값 존재 유무

print(len(train_data)) #리뷰 개수 출력

# 정규 표션식을 통한 한글 외 문자 제거
train_data['document'] = train_data['document'].str.replace('[^ㄱ-ㅎㅏ-ㅣ가-힣]','')

train_data[:5] #상위 5개 출력



#불용어 제거 : 형태소 분석기 Okt를 사용하여 각 문장에 대해 일종의 단어내지는 형태소 단위로 나누는 토큰화 수행. 

# 불용어 정의
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'] 

#형태소 분석기 OKT를 사용한 토큰화 작업(시간 다소 소요)
okt = Okt()

tokenized_data = []
for sentence in tqdm(train_data['document']):
    tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
    stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
    tokenized_data.append(stopwords_removed_sentence)
    
#리뷰 길이 분포 확인
print('리뷰의 최대길이 : ', max(len(review) for review in tokenized_data))
print('리뷰의 평균 길이 : ', sum(map(len, tokenized_data))/len(tokenized_data))
plt.hist([len(review) for review in tokenized_data], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()

