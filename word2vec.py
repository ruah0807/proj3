### Gensim 라이브러리를 사용한 word2vec ###

from gensim.models import Word2Vec

sentences = [
    ['I', 'love', 'machine', 'learning'],
    ['Word2Vec', 'is', 'a', 'technique', 'for', 'word', 'embedding'],
    ['It', 'is', 'widely', 'used', 'in', 'natural', 'language', 'processing']
]

#Word2Vec 모델 학습
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=0)

# 단어 벡터 확인
vector = model.wv['Word2Vec']
print(vector)

#유사한 단어 찾기
similar_words = model.wv.most_similar('Word2Vec')
print(similar_words)