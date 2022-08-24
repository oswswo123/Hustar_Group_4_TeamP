import numpy as np
import pandas as pd
import torch
import os
import re
import random
from pdfminer.high_level import extract_text


def pdf2text(folderpath):
    for file in os.listdir(folderpath):
        txtfile = file.replace("pdf","txt")
        text = extract_text(file)
        with open(txtfile, 'w') as f:
            f.writelines(text)


def preprocessing(dataset):
    company = pd.read_csv('./data/inference_dataset.csv')
    company = company['company'].unique()

    companies = pd.read_csv('./data/stock_master.csv')
    companies = companies['3S']

    com = np.concatenate((company, companies))
    com = np.unique(com)

    articles = []
    for article in dataset['article']:
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
    dataset['article'] = processed
    return dataset


def soft_voting(probabilities):
    return np.mean(probabilities, axis=0, dtype=np.float64)    


def save_csv_file(data_file_path, save_file_path, probabilities):
    ensemble_prob = np.mean(probabilities, axis=0, dtype=np.float64)
    ensemble_pred = (ensemble_prob > 50).astype(np.int32)

    inference_dataframe = pd.read_csv(data_file_path)

    convert_pred = list(map(lambda x: "매수" if x == 1 else "매도", ensemble_pred))
    convert_prob = list(map(lambda x: np.round(x, 2) if x > 50 else np.round(100 - x, 2), ensemble_prob))

    inference_dataframe["predictions"] = convert_pred
    inference_dataframe["pred_rate"] = convert_prob
    inference_dataframe.to_csv(save_file_path, index=False)


def flat_accuracy(preds, labels):
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    
    return np.sum(pred_flat == labels_flat) / len(labels_flat)


def set_seed(seed_val=42):
    random.seed(seed_val)
    np.random.seed(seed_val)
    torch.manual_seed(seed_val)
    torch.cuda.manual_seed_all(seed_val)