# %% 정수 인코딩(Integer Encoding)
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

raw_text = """A barber is a person. a barber is good person. a barber is huge person.
he Knew A Secret! The Secret He Kept is huge secret. Huge secret. His barber kept his word.
a barber kept his word. His barber kept his secret. But keeping and keeping such a huge secret to himself was driving the barber crazy.
the barber went up a huge mountain."""

# 문장 토큰화
sentences = sent_tokenize(raw_text)
print(sentences)

vocab = dict()
preprocessed_sentences = list()
stop_words = set(stopwords.words("english"))

for sentence in sentences:
    # 단어 토큰화
    tokenized_sentence = word_tokenize(sentence)
    result = list()
    
    for word in tokenized_sentence:
        word = word.lower()     # 모든 단어를 소문자화하여 단어의 개수를 줄임
        if word not in stop_words:      # 단어 토큰화 된 결과에서 불용어 제거
            if len(word) > 2 :      # 단어의 길이가 2 이하인 경우에 대해서 추가로 단어를 제거
                result.append(word)
                if word not in vocab:
                    vocab[word] = 0
                vocab[word] += 1
    preprocessed_sentences.append(result)
print(preprocessed_sentences)

print("단어 집합 : ", vocab)

# 빈도수 높은 순서대로 정렬
vocab_sorted = sorted(vocab.items(), key = lambda x:x[1], reverse = True)
print(vocab_sorted)

# 높은 빈도수를 가진 단어일수록 낮은 정수 부여

word_to_index = dict()
integer = 0
for (word, frequency) in vocab_sorted:
    if frequency > 1:       # 빈도수가 작은 단어는 제외
        integer += 1
        word_to_index[word] = integer

print(word_to_index)

vocab_size = 5

# 인덱스가 5 초과인 단어 제거
words_frequency = [word for word, index in word_to_index.items() if index >= vocab_size + 1]

# 해당 단어에 대한 인덱스 정보를 삭제
for w in words_frequency:
    del word_to_index[w]
print(word_to_index)

# 단어 set에 존재하지 않는 상황을 Out-Of-Vocabulary 문제라고 함.
# OOV 문제 해결을 위해 단어집에 OOV란 단어를 추가하고, 단어 집합에 없는 단어를 OOV의 인덱스로 인코딩
word_to_index["OOV"] = len(word_to_index) + 1
print(word_to_index)

encoded_sentences = list()
for sentence in preprocessed_sentences:
    encoded_sentence = list()
    for word in sentence:
        try:
            # 단어 집합에 있는 단어라면 해당 단어의 인코딩 값을 return
            encoded_sentence.append(word_to_index[word])
        except KeyError:
            # 만약 단어 집합에 없는 단어라면 "OOV"의 인코딩 값을 return
            encoded_sentence.append(word_to_index["OOV"])
    encoded_sentences.append(encoded_sentence)
print(encoded_sentences)

# %% Counter 사용하기

from collections import Counter

all_words_list = sum(preprocessed_sentences, list())
print(all_words_list)

# 파이썬의 Counter 모듈을 이용하여 단어의 빈도 수 카운트
vocab = Counter(all_words_list)
print(vocab)

vocab_size = 5
vocab = vocab.most_common(vocab_size)       # 등장 빈도 수가 높은 5개의 단어만 저장
print(vocab)

# integer encoding
word_to_index = dict()
integer = 0
for (word, frequency) in vocab:
    integer += 1
    word_to_index[word] = integer

print(word_to_index)

# %% nltk의 FreqDist 사용하기

from nltk import FreqDist
import numpy as np

# np.hstack으로 문장 구분을 제거
vocab = FreqDist(np.hstack(preprocessed_sentences))

vocab_size = 5
vocab = vocab.most_common(vocab_size)       # 등장 빈도 수가 높은 5개의 단어만 저장
print(vocab)

# enumerate를 사용하여 코드 압축
word_to_index = {word[0] : index + 1 for index, word in enumerate(vocab)}
print(word_to_index)

# %% enumerate 이해하기
'''
    enumerate()는 순서가 있는 자료형을 입력으로 받아 index를 순차적으로 함께 리턴함
'''

# %% Keras의 텍스트 전처리

from tensorflow.keras.preprocessing.text import Tokenizer

tokenizer = Tokenizer()

# fit_on_texts()안에 코퍼스를 입력으로 하면 빈도수를 기준으로 단어 집합을 생성
tokenizer.fit_on_texts(preprocessed_sentences)

print(tokenizer.word_index)     # 각 단어의 빈도수가 높은 순서대로 index 부여
print(tokenizer.word_counts)    # 각 단어가 몇 개인지 출력
print(tokenizer.texts_to_sequences(preprocessed_sentences))     # 코퍼스에 대해서 정수 인코딩

# %% Keras의 most_common()

vocab_size = 5
tokenizer = Tokenizer(num_words = vocab_size + 1)   # 상위 5개의 단어만 사용
tokenizer.fit_on_texts(preprocessed_sentences)

print(tokenizer.word_index)
print(tokenizer.word_counts)    # num_words를 정해도 여전히 13개 단어 다 나옴
print(tokenizer.texts_to_sequences(preprocessed_sentences))  # 실제 적용은 이 메서드를 쓸 때 적용
# OOV는 정수 인코딩 과정에서 삭제됨

# %% Keras에서 OOV 보존하는 방법

vocab_size = 5
tokenizer = Tokenizer(num_words = vocab_size + 2, oov_token = "OOV")    # 숫자 0과 OOV를 고려하여 크기는 +2
tokenizer.fit_on_texts(preprocessed_sentences)

# keras의 OOV 인덱스는 기본적으로 1
print("keras 단어 OOV의 인덱스 : {}".format(tokenizer.word_index["OOV"]))

print(tokenizer.texts_to_sequences(preprocessed_sentences))