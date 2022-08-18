import pandas as pd
import numpy as np
import re
from konlpy.tag import Mecab

inferencedataset = pd.read_csv('report_dataset.csv')
company = inferencedataset['company'].unique()

companies = pd.read_csv('/home/piai/mecab-ko-dic/user-dic/stock_master.csv')
companies = companies['3S']

com = np.concatenate((company, companies))
com = np.unique(com)

articles = []
for article in inferencedataset['article']:
    article = re.sub("\([^)]*\d{6}[^)]*\)", " ", article)
    article = re.sub("\n", " ", article)
    for c in com: # 기업명 제거
        article = re.sub(f"{c}", " ", article)
    articles.append(article)

processed = []
for article in articles:
    article = re.sub("\n", " ", article)
    article = re.sub("\d{6}", " ", article)
    article = re.sub("\[(.*?)\]", " ", article)
    article = re.sub("\w*㈜\w*", " ", article)
    article = re.sub("[^ ~!?△▽▲▼(),./+&₩$%a-zA-Z가-힣0-9]"," ", article)
    article = re.sub(" {1}에 {1}", " ", article)
    article = re.sub(" {1}가 {1}", " ", article)
    article = re.sub(" {1}의 {1}", " ", article)
    article = re.sub(" {1}은 {1}", " ", article)
    article = re.sub(" {1}는 {1}", " ", article)
    article = re.sub("(?<=\d) 억", "억", article)
    article = re.sub("(?<=\d) 조", "조", article)
    article = re.sub("(?<=\d) 원", "원", article)
    article = re.sub("(?<=\d) 년", "년", article)
    article = re.sub("(?<=\d) 월", "월", article)
    article = re.sub("(?<=\d) 배", "배", article)
    article = re.sub("(?<=\d) 분기", "분기", article)
    article = re.sub("(?<=\d) 달러", "달러", article)
    article = re.sub("(?<=\d) 개월", "개월", article)
    article = re.sub(" +", " ", article)
    processed.append(article)

inferencedataset['article']=processed
inferencedataset.to_csv('inferencedatasetprocessed.csv', index=False)