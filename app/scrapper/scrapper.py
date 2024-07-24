import requests
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


class VascoScrapper:
    def __init__(self):
        self.basic_url = "https://www.supervasco.com"
        self.obtained_page = pd.DataFrame(columns=['datetime', 'title', 'link'])
        self.commentaries = pd.DataFrame(columns=['pg_index', 'commentary_source', 'commentary'])
        self.hrefs = {'count': 0, 'hrefs': []}

    def get_all_news_in_page(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")

        page_titles = soup.select(".latest-news-inner > ul li")
        for title in page_titles:
            try:
                comment_count = int(title.select_one('small').text.strip('\n'))
            except Exception:
                comment_count = 0
            if comment_count > 0:
                self.hrefs['count'] += comment_count
                self.hrefs['hrefs'].append(title.select_one('a').attrs['href'])

    def get_min_x_news(self, quantity, page=1):
        content = requests.get(f'{self.basic_url}/ultimas-noticias-vasco/?page={page}')
        html_content = content.text

        self.get_all_news_in_page(html_content)

        if quantity > self.hrefs['count']:
            self.get_min_x_news(quantity, page+1)

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

    def get_facebook_commentaries(self, driver):
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[data-testid="fb:comments Facebook Social Plugin"]')
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 5).until(
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

        commentaries_dict = {
            'pg_index': [],
            'commentary_source': [],
            'commentary': []
        }
        pg_index = self.obtained_page.index[-1]
        for tag in tags:
            commentaries_dict['pg_index'].append(pg_index)
            commentaries_dict['commentary_source'].append('supervasco')
            commentaries_dict['commentary'].append(tag.text)
        
        commentaries_df = pd.DataFrame(commentaries_dict)
        self.commentaries = pd.concat([self.commentaries, commentaries_df])

    def get_page_metadata(self, driver, additional_href):
        title_elem = driver.find_element(By.XPATH, '//meta[@property="og:title"]')
        title = title_elem.get_attribute('content')

        date_elem = driver.find_element(By.CSS_SELECTOR, 'meta[property="article:published_time"]')
        date = date_elem.get_attribute('content')

        new_data = pd.DataFrame({
            'datetime': date,
            'title': title,
            'link': additional_href
        }, index=[self.obtained_page.shape[0]])

        self.obtained_page = pd.concat([self.obtained_page, new_data])

    def get_page_data(self, additional_href):
        options = Options()
        options.add_argument('-headless')

        with Firefox(options=options) as driver:
            driver.get(f"{self.basic_url}{additional_href}")
            # disabled until I go back to brazil
            # try:
            #     fb = self.get_facebook_commentaries(driver)
            # except:
            #     fb = []
            # driver.switch_to.parent_frame()
            self.get_page_metadata(driver, additional_href)

            self.get_supervasco_commentaries(driver)
