from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import json

driver = webdriver.Chrome(executable_path='/Users/aetsyss/Downloads/chromedriver')
driver.get('https://mvideo.ru/')

# Close the pop over
try:
    # Wait for the popover
    popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-popup__block')))
    action = webdriver.common.action_chains.ActionChains(driver)
    # Click on the site logo to close the popover
    action.move_to_element_with_offset(driver.find_element_by_xpath('//a[@class="header-main__logo"]'), 0, 0)
    action.click()
    action.perform()
except TimeoutException:
    print("No popup found.")

# Scroll to Новинки section
novinki = driver.find_element_by_xpath('//ul[contains(@data-init-param, "Новинки")]')
driver.execute_script("arguments[0].scrollIntoView();", novinki)
time.sleep(1)

# Press arror right as long as it exists
while True:
    next = driver.find_elements_by_xpath("//ul[contains(@data-init-param, 'Новинки')]/../../a[@class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right']")
    if len(next) == 0:
        break
    next[0].click()
    time.sleep(5)

# Select all product
products = driver.find_elements_by_xpath('//ul[contains(@data-init-param, "Новинки")]//a[contains(@class, "fl-product-tile-picture")]')
print(len(products))
print('products: ', products)

# Create an array of objects
array = []
for product in products:
    data_product_info = product.get_attribute('data-product-info')
    obj = json.loads(data_product_info)

    info = {
        'id': obj['productId'],
        'name': obj['productName'],
        'price': obj['productPriceLocal']
    }
    array.append(info)

print('array: ', array)