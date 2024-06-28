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

def get_facebook_commentaries(driver):
    iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[data-testid="fb:comments Facebook Social Plugin"]')
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, '_5mdd'))
    )
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup.prettify()

def get_supervasco_commentaries(driver):
    driver.switch_to.frame('id_iframe_comment')
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    return soup.prettify()

def get_commentaries(additional_href):
    options = Options()
    options.add_argument('-headless')

    with Firefox(options=options) as driver:
        driver.get(f"{basic_url}{additional_href}")
        fb = get_facebook_commentaries(driver)
        driver.switch_to.parent_frame()
        vs = get_supervasco_commentaries(driver)

    #     iframe = driver.find_element(By.ID, 'id_iframe_comment')
    #     driver.switch_to.frame('id_iframe_comment')

    #     html = driver.page_source
    #     soup = BeautifulSoup(html, "html.parser")

    with open('fb.html', 'w') as file:
        file.write(fb)
    # with open('vs.html', 'w') as file:
    #     file.write(vs)
    
    print('done')