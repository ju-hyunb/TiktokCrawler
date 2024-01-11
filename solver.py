import os
import sys
import time
import cv2 as cv
import numpy as np

from time import sleep
from collections import Counter

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
#from selenium_move_cursor.MouseActions import move_to_element_chrome

class TikTok():
	
    def DetactCaptcha(self, driver):
        self.driver = driver
        try:
            self.driver.find_element(By.ID,"captcha-verify-image")
            while 1:
                answer = self.solve_captcha()
                if answer['success']:
                    break
                sleep(4)
				
        except Exception as e:
            pass


    def solve_captcha(self):
        try:
            img = self.driver.find_element(By.ID, "captcha-verify-image")
            if img.get_attribute('src'):
                sleep(1)
                img.screenshot('foo.png')
        except Exception as e:
            raise e
        
        img = cv.imread('foo.png')
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        corners = cv.goodFeaturesToTrack(gray,15,0.05,1)
        corners = np.int0(corners)

        x_Array = []
        for i in corners:
            x,y = i.ravel()
            cv.circle(img, (x,y), 3, 355, -1)
            if x > 70:
                x_Array.append(x)


        x_Array.sort()
        print(x_Array)

        slider = self.driver.find_element(By.CLASS_NAME,"captcha_verify_slide--slidebar")
        source = self.driver.find_element(By.CLASS_NAME,"secsdk-captcha-drag-icon")
        source_location = source.location
        source_size = source.size

        array = [170, 345, 400, 400, 345]
        unic = Counter(x_Array)
        for x in x_Array:
            if unic[x] > 1:
                x_offset = x-8
                break

        y_offset = 0
        action = ActionChains(self.driver)
        try:
            steps_count=5
            step = (x_offset)/steps_count
            act_1 = action.click_and_hold(source)
            for x in range(0, steps_count):
                act_1.move_by_offset(step, y_offset)
            act_1.release().perform()

            msg = self.driver.find_element(By.CLASS_NAME, 'msg').find_element(By.TAG_NAME, 'div').text
            while msg == '':
                msg = self.driver.find_element(By.CLASS_NAME, 'msg').find_element(By.TAG_NAME, 'div').text
            print(msg)

            if '인증완료' in msg or 'complete' in msg:
                return {'success': 1}
            else:
                return {'success': 0}
            
        except Exception as e:
            print(e)