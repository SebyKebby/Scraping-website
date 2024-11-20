import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
os.environ['PATH'] += r"E:/ML Learning/NCKH/.venv/chromedriver-win64"
driver = webdriver.Chrome(options=chrome_options)

driver.implicitly_wait(3)

driver.get("https://www.marriott.com/en-us/hotels/cxrwi-the-westin-resort-and-spa-cam-ranh/overview/")





# driver.find_element(By.XPATH,"//button[@class='cookies-eu-ok js-cookies-eu-ok']").click()

# driver.implicitly_wait(3)

# elements = []
# elements = driver.find_elements(By.XPATH,'//tr//td//a[@href]')
# elements = []
# elements = driver.find_elements(By.XPATH,'//tr//td//a[@href]')
# for i in range(len(elements)):
#     text = elements[i].text
#     text = text.replace('.', '')
#     text = text.replace(',', '')
#     text = text.replace('&', 'and')
#     text = text.replace("'", '')
#     text = text.replace(' ', '-')
#     elements[i] = text


# for i in range (1,2) :
#     driver.get('https://www.csrhub.com/search/industry/Hotels-Motels-and-Restaurants?page={}'.format(i))
#     for e in range(len(elements)) :
#         driver.get('https://www.csrhub.com/CSR_and_sustainability_information/{}'.format(elements[e]))
#     driver.execute_script("window.history.go(-1)")