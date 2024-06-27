import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

basic_url = "https://www.supervasco.com"


def get_all_news():
    page = requests.get(basic_url)
    html_content = page.text

    soup = BeautifulSoup(html_content, "html.parser")

    page_titles = soup.select("h4 a")

    page_attrs = map(lambda title: title.attrs, page_titles)

    return list(page_attrs)


def get_specific_new(additional_href):
    page = requests.get(f"{basic_url}{additional_href}")
    html_content = page.text

    soup = BeautifulSoup(html_content, "html.parser")

    page_title = soup.select_one("h1").text
    page_text_html = soup.select("#lightgallery > p")

    print(f"\n{page_title}\n")
    for html in page_text_html:
        if html.text != "":
            print(html.text)

def get_commentaries(additional_href):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    
    with Chrome(options=chrome_options) as browser:
        browser.get(f"{basic_url}{additional_href}")

        # WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "pb-3"))
        # )

        # Get the updated page source
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

    with open('file.html', 'w') as file:
        file.write(soup.prettify())
    
    print('done')