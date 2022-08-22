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

def translatetoen(articles):
    bt_en = []
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    browser.get('https://papago.naver.com/?sk=ko&tk=en')
    wait = WebDriverWait(browser, 10)
    time.sleep(2)
    textbox = browser.find_element(by=By.XPATH, value="//*[@id='txtSource']")
    for article in articles:
        try:
            textbox.send_keys(article)
            time.sleep(5)
            text = browser.find_element(by=By.XPATH, value="//*[@id='txtTarget']/span").text
            bt_en.append(text)
            textbox.clear()
        except:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='txtTarget']/span")))
            text = element.text
            if text == '...':
                time.sleep(3)
                text = browser.find_element(by=By.XPATH, value="//*[@id='txtTarget']/span").text
            bt_en.append(text)
            textbox.clear()
    return bt_en

def translatetokor(bt_en):
    translated_en=[]
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    browser.get('https://papago.naver.com/?sk=en&tk=ko')
    wait = WebDriverWait(browser, 10)
    time.sleep(2)
    textbox = browser.find_element(by=By.XPATH, value="//*[@id='txtSource']")
    for article in bt_en:
        try:
            textbox.send_keys(article)
            time.sleep(5)
            text = browser.find_element(by=By.XPATH, value="//*[@id='txtTarget']/span").text
            translated_en.append(text)
            textbox.clear()
        except:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='txtTarget']/span")))
            text = element.text
            if text == '...':
                time.sleep(3)
                text = browser.find_element(by=By.XPATH, value="//*[@id='txtTarget']/span").text
            translated_en.append(text)
            textbox.clear()
    return translated_en

data = pd.read_csv('traindataset.csv')
articles = data['article']
bt_en = translatetoen(articles)
translated_en = translatetokor(bt_en)
data['article'] = translated_en
data.to_csv('backtranslated_en.csv')
