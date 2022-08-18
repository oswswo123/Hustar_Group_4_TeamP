import re
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
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

browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) # 크롬드라이버 저장 경로 자동 호출
df = pd.DataFrame(columns=("company", "title", "article", "opinion", "firm", "date"))

for i in range(1,1735):
    df.to_csv('/home/piai/다운로드/information.csv', index=False)
    browser.get(f"https://finance.naver.com/research/company_list.naver?&page={i}")
    time.sleep(1)
    for j in range(0, 6):
        start = 8 * j + 3
        for k in range(start, start+5):
            company = browser.find_element(by=By.XPATH, value=f"//*[@id='contentarea_left']/div[3]/table[1]/tbody/tr[{k}]/td[1]").text
            click = browser.find_element(by=By.XPATH, value=f"//*[@id='contentarea_left']/div[3]/table[1]/tbody/tr[{k}]/td[2]/a")
            title = click.text
            firm = browser.find_element(by=By.XPATH, value=f"//*[@id='contentarea_left']/div[3]/table[1]/tbody/tr[{k}]/td[3]").text
            date = browser.find_element(by=By.XPATH, value=f"//*[@id='contentarea_left']/div[3]/table[1]/tbody/tr[{k}]/td[5]").text
            click.click()
            time.sleep(2)
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            article = ""
            articles = soup.select("#contentarea_left > div.box_type_m.box_type_m3 > table > tbody > tr:nth-child(4) > td > div:nth-child(1)")
            for a in articles:
                article += ("\n" + a.text)
            opinion = soup.find(attrs={"class" : "coment"}).get_text()
            df = df.append({"company":company, "title":title, "article":article, "opinion":opinion, "firm":firm, "date":date}, ignore_index=True)
            print(df.tail())
            browser.back()
            time.sleep(1)
df.to_csv('/home/piai/다운로드/information.csv', index=False)
