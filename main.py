from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests as rq
from bs4 import BeautifulSoup as bs

# Constants
google_form_add = 'https://forms.gle/XJoPpSE59L4VdvMs7'
zillow_url = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C' \
             '%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A' \
             '-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C' \
             '%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A' \
             '%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse' \
             '%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B' \
             '%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D' \
             '%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min' \
             '%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D '
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}
# lists
links = []
prices = []
addresses = []


# Data Scraping function
def keep_searching():
    response = rq.get(url=zillow_url, headers=HEADERS)
    zillow_web_page = response.text
    soup = bs(zillow_web_page, 'html.parser')
    price_list = soup.find_all('div', {"class": "list-card-price", })
    add_list = soup.find_all('address', {"class": 'list-card-addr'})
    link_list = soup.find_all('a', {'class':'list-card-link list-card-link-top-margin'})
    if price_list is None and add_list is None and link_list is None:
        return False
    else:
        for i in price_list:
            prices.append(i.text.split("/")[0].lstrip("$").replace(',', '').split('+')[0])
        for i in add_list:
            addresses.append(i.text)
        for i in link_list:
            links.append(i['href'])


# Loop to check returned value
counter = 0
while keep_searching() is False and counter < 15:
    counter += 1
    keep_searching()
# Editing elements
links[2] = f"https://www.zillow.com{links[2]}"
links[5] = f"https://www.zillow.com{links[5]}"
# Setting up selenium
service = Service("C:/Users/HP/chromedriver_win32/chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)
# Getting google from link
driver.get(google_form_add)
# writing in details automatically
for i in range(len(links)):
    driver.implicitly_wait(5)
    date = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    driver.execute_script(f"arguments[0].setAttribute('value', '{addresses[i]}')", date)
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').click()
    driver.find_element(By.XPATH,
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(addresses[i])
    driver.find_element(By.XPATH,
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(prices[i])
    driver.find_element(By.XPATH,
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(links[i])
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').click()
    driver.implicitly_wait(3)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
driver.quit()

