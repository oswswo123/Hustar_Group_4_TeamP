# %% 패딩(Padding)
'''
    컴퓨터는 길이가 전부 동일한 문서들에 대해서는 하나의 행렬로 보고 한꺼번에 묶어서 처리가 가능.
    병렬 연산을 위해서 여러 문장의 길이를 임의로 동일하게 맞춰주는 작업이 Padding
'''


import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer

preprocessed_sentences = [["barber", "person"], ["barber", "good", "person"], ["barber", "huge", "person"],
                          ["knew", "secret"], ["secret", "kept", "huge", "secret"], ["huge", "secret"], ["barber", "kept", "word"],
                          ["barber", "kept", "word"], ["barber", "kept", "secret"], ["keeping", "keeping", "huge", "secret", "driving", "barber", "crazy"],
                          ["barber", "went", "huge", "mountain"]]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(preprocessed_sentences)
encoded = tokenizer.texts_to_sequences(preprocessed_sentences)
print(encoded)

# 모두 동일한 길이로 맞춰주기 위해서 가장 긴 문장의 길이 측정
max_len = max(len(item) for item in encoded)
print("최대 길이 : ", max_len)

for sentence in encoded:
    while len(sentence) < max_len:
        sentence.append(0)

padded_np = np.array(encoded)
print(padded_np)

# %% Keras로 Padding

from tensorflow.keras.preprocessing.sequence import pad_sequences

encoded = tokenizer.texts_to_sequences(preprocessed_sentences)
print(encoded)

padded = pad_sequences(encoded)     # 기본적으로 0을 앞에서부터 채움.
print(padded)

padded = pad_sequences(encoded, padding="post")     # 이러면 뒤에서부터 0을 채움
print(padded)

# 문장을 길이 5를 기준으로 패딩
# 5보다 짧으면 zero padding, 5보다 길었으면 데이터 손실
# 데이터 손실의 경우 앞의 단어가 사라짐
padded = pad_sequences(encoded, padding="post", maxlen=5)
print(padded)

# 데이터 손실을 뒤의 단어가 먼저 되게 하려면
padded = pad_sequences(encoded, padding="post", truncating="post", maxlen=5)
print(padded)