from selenium import webdriver
import matplotlib.pyplot as plt
import numpy as np
import time
from selenium.webdriver.common.keys import Keys
import urllib.request
from selenium.webdriver.common.by import By

def iniciaCor(color):
    color.append(['green','c:G commander:G' ])
    color.append(['Red','c:R commander:R' ])
    color.append(['White','c:W commander:W' ])
    color.append(['Blue','c:U commander:U' ])
    color.append(['Black','c:B commander:B' ])
    return color
def MiningColor(color):
    link = 'https://scryfall.com'
    navegador = webdriver.Firefox(executable_path = r'C:\Users\Blade\anaconda3/geckodriver')
    driver = webdriver.Firefox(executable_path = r'C:\Users\Blade\anaconda3/geckodriver')
    driver.get(link)
    navegador.get(link)
    input_ = navegador.find_element(By.TAG_NAME,'input')
    input_.send_keys(color[1]+' legal:legacy')
    input_.send_keys(Keys.ENTER)
    L = 60
    j = 0
    div = 0.04
    while(div<1):
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight*%s);"% div)
        time.sleep(1)
        div += 0.04
    for i in range(55,59):
        print(i)
        if(i%60==0 and i!=0):
            if(j==0):
                navegador.find_element(By.XPATH,'/html/body/div[3]/div[4]/div/div[2]/a[1]').click()
            else:
                navegador.find_element(By.XPATH,'/html/body/div[3]/div[4]/div/div[2]/a[3]').click()
                while(div<1):
                    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight*%s);"% div)
                    time.sleep(1)
                    div += 0.04
            j += 1
        div = 0.04
        cards = navegador.find_elements(By.CLASS_NAME,"card-grid-item-card")
        link = cards[i-L*j].get_attribute('href')
        driver.get(link)
        time.sleep(2)
        src = driver.find_element(By.CLASS_NAME,"card-image-front").find_element(By.TAG_NAME,"img").get_attribute("src")
        driver.get(src)
        time.sleep(2)
        name = color[0]+str(i)+'.jpg'
        urllib.request.urlretrieve(src, "./img/"+name)
    navegador.quit()
    driver.quit()

cores = []
cores = iniciaCor(cores)

for i in range(5):
    MiningColor(cores[i])