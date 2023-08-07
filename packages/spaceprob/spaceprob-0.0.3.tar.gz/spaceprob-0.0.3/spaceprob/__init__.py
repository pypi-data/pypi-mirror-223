from selenium import webdriver
from selenium.webdriver.common.by import By

def getval():
    driver = webdriver.Chrome()
    url = 'https://voyager.jpl.nasa.gov/'
    driver.get(url)
    vals = driver.find_elements(By.ID, "voy1_km")
    return vals[0].text