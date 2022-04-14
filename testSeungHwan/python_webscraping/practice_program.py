# %% 연습하기 (알라딘 베스트셀러 스크래핑 후 csv파일로 출력)

import requests
from bs4 import BeautifulSoup
import csv

filename = "알라딘 베스트셀러.csv"
filepointer = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(filepointer)

# header 출력
title = "순위	책제목	저자	출판사	가격".split("\t")
writer.writerow(title)

rank_counter = 1
for page in range(1, 21):
    url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0&page={}&cnt=1000&SortOrder=1".format(page)
    
    resource = requests.get(url)
    resource.raise_for_status()
    
    soup = BeautifulSoup(resource.text, "lxml")
    
    books = soup.find_all("div", attrs={"class":"ss_book_box"})
    
    for book in books:
        is_hottag = book.find("span", attrs={"class":"ss_ht1"})
        
        if is_hottag:
            book_datas = book.find_all("li")
            # book_datas[1] : 이름
            # book_datas[2] : 저자, 출판사[-2], 출간일[-1]
            # book_datas[3] : 가격, [0]->할인 전 가격, [2]->할인 후 가격, [4]->할인율
            book_name = book_datas[1].get_text()
            book_production_related = book_datas[2].find_all("a")
            book_authors = book_production_related[:-1]
            book_authors_string = ""
            for index, book_author in enumerate(book_authors):
                book_authors_string = book_authors_string + book_author.get_text() + ", "
            book_authors_string = book_authors_string[:-2]
            book_publisher = book_production_related[-1].get_text()
            book_price = book_datas[3].find("span", attrs={"class":"ss_p2"}).get_text()
            
        else:
            book_datas = book.find_all("li")
            # book_datas[0] : 이름
            # book_datas[1] : 저자, 출판사[-2], 출간일[-1]
            # book_datas[2] : 가격, [0]->할인 전 가격, [2]->할인 후 가격, [4]->할인율
            book_name = book_datas[0].get_text()
            book_production_related = book_datas[1].find_all("a")
            book_authors = book_production_related[:-1]
            book_authors_string = ""
            for index, book_author in enumerate(book_authors):
                book_authors_string = book_authors_string + book_author.get_text() + ", "
            book_authors_string = book_authors_string[:-2]
            book_publisher = book_production_related[-1].get_text()
            book_price = book_datas[2].find("span", attrs={"class":"ss_p2"}).get_text()
            
        writer.writerow([rank_counter, book_name, book_authors_string, book_publisher, book_price])
        rank_counter += 1
    
filepointer.close()