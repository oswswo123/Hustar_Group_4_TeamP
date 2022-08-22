from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
chrome_options = Options()
chrome_options.add_argument('--incognito')
# chrome_options.add_argument('--headless')        # Head-less 설정
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-setuid-sandbox')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": '/home/piai/다운로드/reports',
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    }
)

def translatetocn(articles):
    bt_cn = []
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    browser.get('https://papago.naver.com/?sk=ko&tk=zh-CN')
    wait = WebDriverWait(browser, 10)
    time.sleep(2)
    textbox = browser.find_element(by=By.XPATH, value="//*[@id='txtSource']")
    for article in articles:
        try:
            textbox.send_keys(article)
            time.sleep(5)
            text = browser.find_element(by=By.XPATH, value="//*[@id='txtTarget']/span").text
            bt_cn.append(text)
            textbox.clear()
        except:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='txtTarget']/span")))
            text = element.text
            if text == '...':
                time.sleep(3)
                text = browser.find_element(by=By.XPATH, value="//*[@id='txtTarget']/span").text
            bt_cn.append(text)
            textbox.clear()
    return bt_cn

def translatetokor(bt_cn):
    translated_cn=[]
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    browser.get('https://papago.naver.com/?sk=zh-CN&tk=ko')
    wait = WebDriverWait(browser, 10)
    time.sleep(2)
    textbox = browser.find_element(by=By.XPATH, value="//*[@id='txtSource']")
    for article in bt_cn:
        try:
            textbox.send_keys(article)
            time.sleep(5)
            text = browser.find_element(by=By.XPATH, value="//*[@id='txtTarget']/span").text
            translated_cn.append(text)
            textbox.clear()
        except:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='txtTarget']/span")))
            text = element.text
            if text == '...':
                time.sleep(3)
                text = browser.find_element(by=By.XPATH, value="//*[@id='txtTarget']/span").text
            translated_cn.append(text)
            textbox.clear()
    return translated_cn

data = pd.read_csv('traindataset.csv')
articles = data['article']
bt_cn = translatetocn(articles)
translated_cn = translatetokor(bt_cn)
data['article'] = translated_cn
data.to_csv('backtranslated_cn.csv')
