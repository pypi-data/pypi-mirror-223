from selenium import webdriver
from selenium.webdriver.common.by import By

def getval(path):
    driver = webdriver.Chrome(executable_path=path)
    url = 'https://voyager.jpl.nasa.gov/'
    driver.get(url)
    vals = driver.find_elements(By.ID, "voy1_km")
    print(vals[0].text)
    return vals[0].text