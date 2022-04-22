# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 23:59:26 2022

@author: byeonghwa
"""

# Numpy 로 패딩하기
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer

preprocessed_sentences = [['barber', 'person'], ['barber', 'good', 'person'], ['barber', 'huge', 'person'], ['knew', 'secret'], ['secret', 'kept', 'huge', 'secret'], ['huge', 'secret'], ['barber', 'kept', 'word'], ['barber', 'kept', 'word'], ['barber', 'kept', 'secret'], ['keeping', 'keeping', 'huge', 'secret', 'driving', 'barber', 'crazy'], ['barber', 'went', 'huge', 'mountain']]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(preprocessed_sentences)
encoded = tokenizer.texts_to_sequences(preprocessed_sentences)
print(encoded)

max_len = max(len(item) for item in encoded)
print('최대 길이 :',max_len)

for sentence in encoded:
    while len(sentence) < max_len:
        sentence.append(0)

padded_np = np.array(encoded)
print(padded_np)

# 케라스 전처리 도구로 패딩하기

from tensorflow.keras.preprocessing.sequence import pad_sequences

encoded = tokenizer.texts_to_sequences(preprocessed_sentences)
print(encoded)

padded = pad_sequences(encoded)
print(padded)

padded = pad_sequences(encoded, padding='post')
print(padded)

(padded == padded_np).all()


padded = pad_sequences(encoded, padding='post', maxlen=5)
print(padded)

padded = pad_sequences(encoded, padding='post', truncating='post', maxlen=5)
print(padded)

last_value = len(tokenizer.word_index) + 1 # 단어 집합의 크기보다 1 큰 숫자를 사용
print(last_value)

padded = pad_sequences(encoded, padding='post', value=last_value)
print(padded)

