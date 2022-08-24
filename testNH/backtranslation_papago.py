import sys, os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
chrome_options = Options()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')        # Head-less 설정
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-setuid-sandbox')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option('prefs',  {
    # "download.default_directory": '/home/piai/다운로드',
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    }
)

def translate(articles, flanguage):
    translated = []
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    browser.get(f'https://papago.naver.com/?sk=ko&tk={flanguage}')
    wait = WebDriverWait(browser, 10)
    time.sleep(2)
    textbox = browser.find_element(by=By.XPATH, value="//*[@id='txtSource']")
    for article in articles:
        textbox.send_keys(article)
        time.sleep(10)
        text = browser.find_element(by=By.XPATH, value="//*[@id='txtTarget']/span").text
        translated.append(text)
        textbox.clear()
    translated = list(dict.fromkeys(translated)) # 중복 제거
    return translated

def backtranslate(translated, language, flanguage, label):
    backtranslation = []
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    browser.get(f'https://papago.naver.com/?sk={flanguage}&tk=ko')
    time.sleep(2)
    textbox = browser.find_element(by=By.XPATH, value="//*[@id='txtSource']")
    for article in translated:
        textbox.send_keys(article)
        time.sleep(10)
        text = browser.find_element(by=By.XPATH, value="//*[@id='txtTarget']/span").text
        backtranslation.append(text)
        textbox.clear()
    backtranslation = list(dict.fromkeys(backtranslation)) # 중복 제거
    backtranslation_df = pd.DataFrame({'article': backtranslation, 'label': label})
    if label == 0:
        name = 'sell'
    else:
        name = 'buy'
    backtranslation_df.to_csv(f"{name}_backtranslated_papago_{language}.csv")
    return backtranslation

def main():
    json_file = open("./backtranslation_config.json", encoding="utf-8")
    key_dict = json.loads(json_file.read())
    data_file_path = key_dict["data_file_path"]
    language = key_dict["language"]
    if language == "English":
        flanguage = "en"
    elif language == "Chinese":
        flanguage = "zh-CN"

    data = pd.read_csv(data_file_path)
    sell = data[data['label'] == 0].article
    buy = data[data['label'] == 1].article
    sell.reset_index(drop=True, inplace=True)
    buy.reset_index(drop=True, inplace=True)

    translate_sell = translate(sell, flanguage)
    backtranslate(translate_sell, language, flanguage, 0)
    translate_buy = translate(buy, flanguage)
    backtranslate(translate_buy, language, flanguage, 1)


if __name__ == "__main__":
    main()