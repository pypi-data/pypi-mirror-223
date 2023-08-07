from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

url = 'https://voyager.jpl.nasa.gov/'

driver.get(url)

vals = driver.find_elements(By.ID, "voy1_km")
print(vals[0].text)

def getval():
    return vals[0].text