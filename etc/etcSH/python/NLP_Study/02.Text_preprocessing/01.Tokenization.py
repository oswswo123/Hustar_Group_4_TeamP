# %% 영어 토큰화

from nltk.tokenize import word_tokenize
from nltk.tokenize import WordPunctTokenizer
from tensorflow.keras.preprocessing.text import text_to_word_sequence

# word_tokenize 사용
word = "Don't be fooled by the dark sounding name, Mr.Jone's Orphanage is as cheery as cheery goes for a pastry shop."
print("단어 토큰화1 : ", word_tokenize(word))
print("단어 토큰화2 : ", WordPunctTokenizer().tokenize(word))
print("단어 토큰화3 : ", text_to_word_sequence(word))
# 셋의 아포스트로피(')가 들어간 코퍼스의 처리가 다름.
# 필요한 상황에 맞춰 있는 도구를 잘 찾아 쓰자 !

# %% 한글 토큰화 - 실행이 안됨. CUDA 설치해야할듯

import kss

text = """
    딥 러닝 자연어 처리가 재미있기는 합니다.
    그런데 문제는 영어보다 한국어로 할 때 너무 어렵습니다. 이제 해 보면 알걸요?
"""
print("한국어 문장 토큰화 : ", kss.split_sentences(text))

# %% nltk를 활용한 토큰화

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

text = "I am actively looking for Ph.D, students. and you ard a Ph.D. student."
tokenized_sentence = word_tokenize(text)

print("단어 토큰화 : ", tokenized_sentence)
print("품사 태깅 : ", pos_tag(tokenized_sentence))

# %% konlpy를 활용한 토큰화 및 품사태깅

from konlpy.tag import Okt
from konlpy.tag import Kkma

okt = Okt()
kkma = Kkma()

print("OKT 형태소 분석 : ", okt.morphs("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))
print("OKT 품사 태깅 : ", okt.pos("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))
print("OKT 명사 추출 : ", okt.nouns("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))

print("꼬꼬마 형태소 분석 : ", kkma.morphs("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))
print("꼬꼬마 품사 태깅 : ", kkma.pos("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))
print("꼬꼬마 명사 추출 : ", kkma.nouns("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))