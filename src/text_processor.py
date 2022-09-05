import argparse
import pandas as pd
import re
import sys, os
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

sys.path.append(os.path.dirname(__file__))


def preprocessing(data):
    data = re.sub(r'\n', '', data)
    REMOVE_CHARS = re.compile("'+|(=+.{2,30}=+)|__TOC__|(ファイル:).+|:(en|de|it|fr|es|kr|zh|no|fi):", re.UNICODE)
    SPACE_CHARS = re.compile("(\\s|゙|゚|　)+", re.UNICODE)
    EMAIL_PATTERN = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.UNICODE)
    URL_PATTERN = re.compile("(ftp|http|https)?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.UNICODE)
    REMOVE_TOKEN_CHARS = re.compile("(\\*$|:$|^파일:.+|^;)", re.UNICODE)
    MULTIPLE_SPACES = re.compile(' +', re.UNICODE)
    EXCEPT_KOREAN = re.compile("[^ ㄱ-ㅣ가-힣+|.]", re.UNICODE)
    data = re.sub(EMAIL_PATTERN, ' ', data)  # remove email pattern
    data = re.sub(URL_PATTERN, ' ', data) # remove url pattern
    data = re.sub(REMOVE_CHARS, ' ', data)  # remove unnecessary chars
    data = re.sub(EXCEPT_KOREAN, ' ', data)
    data = re.sub(SPACE_CHARS, ' ', data)
    data = re.sub(MULTIPLE_SPACES, ' ', data)
    data = re.sub(' [.]', '', data)
    stop_words = "등 등이 에 에서 와 과 은 는 의 개 개의 년간 로 을 를 하는 총 월 목표주가 현재주가 연결 요약 재무제표 십억원 만주 주 주가 배 년 일 만 억원 우 좌 원 억 백만 약 각각 으로 십 액면가 종가 자본금 발행주식수 시가총액 외국인지분율 일평균거래량 일평균거래대금 주가수익률 절대수익률 상대수익률 배당수익률"
    stop_words = set(stop_words.split(' '))
    result = [word for word in data.split(' ') if not word in stop_words]
    result = " ".join(result)
    return result

def read_pdf_PDFMINER(pdf_file_path):
    """
    pdf_file_path: 'dir/aaa.pdf'로 구성된 path로부터 
    내부의 text 파일을 모두 읽어서 스트링을 리턴함.
    https://pdfminersix.readthedocs.io/en/latest/tutorials/composable.html
    """
    output_string = StringIO()
    with open(pdf_file_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for pageNumber, page in enumerate(PDFPage.create_pages(doc)):
            if pageNumber == 0:
                interpreter.process_page(page)
                break

    return str(output_string.getvalue())

def main():
    parser = argparse.ArgumentParser("Text Pre-process Method.")
    
    parser.add_argument("--file_path", required=True, help="pdf file path")
    
    args = parser.parse_args()
    
    pdf_file_path = args.file_path
    text_data = read_pdf_PDFMINER(pdf_file_path)
    preprocessed_text_data = preprocessing(text_data)    
    
    print(preprocessed_text_data)
    
if __name__ == "__main__":
    main()