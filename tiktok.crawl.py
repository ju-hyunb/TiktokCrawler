import os
import sys
import pandas as pd
import time
import datetime

import requests
from bs4 import BeautifulSoup as bs


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


import warnings
warnings.filterwarnings('ignore')


from solver import TikTok


class Driver:

    def __init__(self) -> None:
        pass
    
    def _StartDriver(self):
		
        service = Service()
        option = webdriver.ChromeOptions()
        
        debugbrowser_remote_address = "127.0.0.1:10001"
        option.add_experimental_option("debuggerAddress", debugbrowser_remote_address)
        driver = webdriver.Chrome(service=service, options=option)
		
        driver.get("https://www.google.com/")
        return driver
    
    def _MoveUrl(self, url):
        
        driver = self._StartDriver()
        driver.get(url)
        time.sleep(1)

        return driver
    

    def ScrollDown_(self):

        SCROLL_PAUSE_CNT = 100
        cnt=0
        while SCROLL_PAUSE_CNT != cnt :

            body = driver.find_element(By.CSS_SELECTOR, 'body')
            body.send_keys(Keys.PAGE_DOWN)

            cnt+=1
            self.SolveCaptcha()



    

    def ScrollDown(self):

        SCROLL_PAUSE_TIME = 10
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:

            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            self.SolveCaptcha()

            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            
            last_height = new_height

   
    def SolveCaptcha(self):
        solver=TikTok()
        solver.DetactCaptcha(driver)




    

class Extracter:

    def __init__(self, driver):
        self.driver = driver

    def FindElementByXpath(self, xpath):
        val = ""
        try:
            val=self.driver.find_element(By.XPATH, xpath)
        except:
            pass
        return val
    
    def FindElementsByXpath(self, xpath):
        val_list = []
        try:
            val_list=self.driver.find_elements(By.XPATH, xpath)
        except:
            pass
        return val_list
    
    def ChildElementByXpath(self, parent, xpath):
        val = ""
        try:
            val=parent.find_element(By.XPATH, xpath)
        except:
            pass
        return val
    
    def ChildElementsByXpath(self, parent, xpath):
        val_list = ""
        try:
            val_list=parent.find_elements(By.XPATH, xpath)
        except:
            pass
        return val_list
    
    def GetAttribute(self, el, attr):
        val = ""
        if el is not None:
            if attr == "text":
                val = el.text
            else:  
                val = el.get_attribute(attr)
        
        return val
    
    def Click(self, el):
        try:
            el.click()
        except:
            print("Couldnt click!")



def ExtractFeedList(driver):

    extracter = Extracter(driver)
    time.sleep(5)
    following = extracter.FindElementByXpath("//strong[@title='팔로잉']")
    following = extracter.GetAttribute(following, "text")

    follower = extracter.FindElementByXpath("//strong[@title='팔로워']")
    follower = extracter.GetAttribute(follower, "text")

    likes = extracter.FindElementByXpath("//strong[@title='좋아요']")
    likes = extracter.GetAttribute(likes, "text")

    print("팔로잉 : ", following, "팔로워 : ", follower, "좋아요 : ", likes)

    Driver.ScrollDown()

    time.sleep(5)

    FeedList=extracter.FindElementsByXpath("//div[@class='css-vi46v1-DivDesContainer eih2qak4']")
    SeedDict = {}
    for idx, feed in enumerate(FeedList):
        idx+=1

        obj = extracter.ChildElementByXpath(feed, ".//div/a")
        title = extracter.GetAttribute(obj, "title")
        url = extracter.GetAttribute(obj, "href")
        SeedDict[idx] = [title, url]

        print(idx, title, url)

    return SeedDict


def Extractmeta(dicts, driver):

    for idx, [title, url] in dicts.items():


        driver = Driver._MoveUrl(url)
        extracter = Extracter(driver)

        login = extracter.FindElementByXpath("//div[@data-e2e='modal-close-inner-button']")
        if login != "":
            extracter.Click(login)
            time.sleep(2)


        body = extracter.FindElementByXpath("//div[@class='css-1rhses0-DivText e1mzilcj1']")
        body = extracter.GetAttribute(body, "text")

        username = extracter.FindElementByXpath("//span[@data-e2e='browse-username']")
        username = extracter.GetAttribute(username, "text")

        nickname = extracter.FindElementByXpath("//span[@data-e2e='browser-nickname']/span[1]")
        nickname = extracter.GetAttribute(nickname, "text")

        writedate = extracter.FindElementByXpath("//span[@data-e2e='browser-nickname']/span[3]")
        writedate = extracter.GetAttribute(writedate, "text")


        print("idx : ", idx)
        print("title : ", title)
        print("url : ", url)
        print("body : ", body)
        print("username : ", username)
        print("nickname : ", nickname)
        print("writedate : ", writedate)
        print("=========================================================")

        time.sleep(1)




    

if __name__ == "__main__":


    account=str(input("Enter the TikTok account you want to crawl!  ex) newjeans_official "))
    
    url = f"https://www.tiktok.com/@{account}"


    Driver = Driver()
    driver = Driver._MoveUrl(url)

    FeedListDict = ExtractFeedList(driver)
    Extractmeta(FeedListDict, driver)
