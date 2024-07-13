import requests
from bs4 import BeautifulSoup
# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import pandas as pd

class VascoScrapper:
    def __init__(self):
        self.basic_url = "https://www.supervasco.com"
        self.obtained_page = pd.DataFrame(columns=['index', 'datetime', 'title', 'link'])
        self.commentaries = pd.DataFrame(columns=['index', 'commentary_source', 'commentary'])
        

# basic_url = "https://www.supervasco.com"


    def get_all_news(self):
        page = requests.get(self.basic_url)
        html_content = page.text

        soup = BeautifulSoup(html_content, "html.parser")

        page_titles = soup.select("h4 a")

        page_attrs = map(lambda title: title.attrs, page_titles)

        return list(page_attrs)


    def get_news_data(self, additional_href):
        page = requests.get(f"{self.basic_url}{additional_href}")
        html_content = page.text

        soup = BeautifulSoup(html_content, "html.parser")

        page_title = soup.select_one("h1").text
        page_text_html = soup.select("#lightgallery > p")

        print(f"\n{page_title}\n")
        for html in page_text_html:
            if html.text != "":
                print(html.text)


    def get_extracted_page_data(self, driver):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        print(html.page_title)


    def get_facebook_commentaries(self, driver):
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[data-testid="fb:comments Facebook Social Plugin"]')
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, '_5mdd'))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.select('._5mdd span')
        return [('facebook', tag.get_text(separator=' ')) for tag in tags]

    def get_supervasco_commentaries(self, driver):
        driver.switch_to.frame('id_iframe_comment')
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        tags = soup.select('.pb-3 > p')
        return [('supervasco', tag.text) for tag in tags]

    def get_commentaries(self, additional_href):
        options = Options()
        options.add_argument('-headless')

        with Firefox(options=options) as driver:
            driver.get(f"{self.basic_url}{additional_href}")
            try:
                fb = self.get_facebook_commentaries(driver)
            except:
                fb = []
            driver.switch_to.parent_frame()
            vs = self.get_supervasco_commentaries(driver)
            print(fb)
            print('\n')
            print(vs)

        
        print('done')