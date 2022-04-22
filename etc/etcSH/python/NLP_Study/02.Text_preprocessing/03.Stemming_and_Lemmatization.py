# %% 어간 추출(Stemming) and 표제어 추출(Lemmatization)\
# %% Lemmatization

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

words =  ["policy", "doing", "organization", "have", "going", "love", "lives", "fly", "dies", "watched", "has", "starting"]

print("표제어 추출 전 : ", words)
print("표제어 추출 후 : ", [lemmatizer.lemmatize(word) for word in words])
# ha, dy같은 의미불명 단어가 나옴
# Lemmatization은 본래 단어의 품사정보를 알아야만 정확한 결과를 얻을 수 있음

print(lemmatizer.lemmatize("dies", "v"))
print(lemmatizer.lemmatize("watched", "v"))
print(lemmatizer.lemmatize("has","v"))

# %% Stemming

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

stemmer = PorterStemmer()
sentence = """
This was not the map we found in Billy Bones's chest, but an accurate copy, complete in all things--names
and heights and soundings--with the single exception of the red crosses and the written notes.
"""
tokenized_sentence = word_tokenize(sentence)

print("어간 추출 전 : ", tokenized_sentence)
print("어간 추출 후 : ", [stemmer.stem(word) for word in tokenized_sentence])

