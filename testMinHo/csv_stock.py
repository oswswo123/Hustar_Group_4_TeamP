# File Name: csv_stock.py
# File Contents: Practice for Web crawling
# Programmed By Minho Kim 2022.04.14 (Thu)

import csv
from wsgiref.util import request_uri
import requests
from bs4 import BeautifulSoup

#Naver 금융 URL 주소
url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="

#File name 및 쓰기 설정
filename = "Naver_Kospi_top_200.csv"
f = open(filename, 'w', encoding="utf-8-sig", newline="")
writer = csv.writer(f)

# csv 파일 타이틀 추가
title = "N	종목명	현재가	전일비	등락률	액면가	시가총액	상장주식수	외국인비율	거래량	PER	ROE".split("\t")
writer.writerow(title)

# Data를 담기 위한 리스트 선언
data_list = []

# Page 돌면서 Table Data를 List에 추가
for page in range(1,5):
    res = requests.get(url + str(page))
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    # 웹 페이지 중 표에 해당하는 내용만 찾기
    data_rows = soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr") 
    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1:   #의미없는 데이터 스킵
            continue
        data = [col.get_text().strip() for col in columns]  #불필요한 탭문자 삭제
        data_list.append(data)

# Data List를 등락률을 기준으로 내림차순 정렬
data_list.sort(key= lambda x: float(x[4][:-1]), reverse=True)

# csv 파일에 쓰기
for data in data_list:
    writer.writerow(data)