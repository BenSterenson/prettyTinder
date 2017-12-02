import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Tinder(object):
    BTN_FB_LOGIN_STR = "Log in with Facebook"
    BTN_PHONE_LOGIN_STR = "Log in with phone number"
    BTN_NEXT_STR = "Next"
    TIME_OUT = 5


    def __init__(self, phone='', email='', password='', chrome_driver=os.path.join(os.getcwd(), "chromedriver.exe")):
        self.email = email
        self.password = password
        self.phone = phone.split()
        self.chrome_driver = chrome_driver
        self.driver = webdriver.Chrome(self.chrome_driver)
        self.driver.get('http://www.tinder.com')
        time.sleep(5)


    def wait_for_load(self, inputXPath):
        Wait = WebDriverWait(self.driver, self.TIME_OUT)
        Wait.until(EC.presence_of_element_located((By.XPATH, inputXPath)))
        Wait.until(EC.element_to_be_clickable((By.XPATH, inputXPath)))

    
    def click_btn_by_str(self, btn_str):
        login_button = self.driver.find_elements_by_xpath("//*[contains(text(), \'" + btn_str + "\')]")[0]
        login_button.click()


    def fb_connect(self):       
        main_window_handle = self.driver.current_window_handle
        
        # Click Log in with Facebook
        self.click_btn_by_str(self.BTN_FB_LOGIN_STR)
        
        # Switch window
        signin_window_handle = None
        while not signin_window_handle:
            for handle in self.driver.window_handles:
                if handle != main_window_handle:
                    signin_window_handle = handle
                    break
        
        self.driver.switch_to.window(signin_window_handle)
        
        # Fill email
        email_id = self.driver.find_element_by_id("email")
        email_id.clear()
        email_id.send_keys(self.email)
        
        # Fill Password
        pass_id = self.driver.find_element_by_id("pass")
        pass_id.clear()
        pass_id.send_keys(self.password)
        
        # Click Login
        login_btn_id = self.driver.find_element_by_name("login")
        login_btn_id.send_keys(Keys.RETURN)

        self.driver.switch_to.window(main_window_handle)
        time.sleep(self.TIME_OUT)


    def frame_search(self, frame_number):
        frame_counter = 0
        for child_frame in self.driver.find_elements_by_tag_name('iframe'):
            if frame_counter == frame_number:
                self.driver.switch_to.frame(child_frame)
            frame_counter += 1


    def phone_connect(self):

        # Click Log in with phone number
        self.click_btn_by_str(self.BTN_PHONE_LOGIN_STR)

        # Change frame
        self.frame_search(frame_number=1)
        time.sleep(2)

        # Change Country code
        country_code_id = self.driver.find_element_by_id("u_0_6p")
        self.driver.execute_script("arguments[0].value = arguments[1]", country_code_id, self.phone[0])
        
        # Input Phone Number
        search_box = self.driver.find_element_by_name('phone_number')
        search_box.send_keys(self.phone[1])
        
        # Press Next
        next_button = self.driver.find_elements_by_xpath("//*[contains(text(), \'" + self.BTN_NEXT_STR + "\')]")[-1]
        next_button.click()

    def click_next_btn(self):
        for next_btn in self.driver.find_elements_by_xpath("//*[contains(text(), 'Next')]"):
            try:
                next_btn.click()
            except:
                continue
    
    def wait_for_clickable(self, by_type ,identifier):
        Wait = WebDriverWait(self.driver, self.TIME_OUT)       
        Wait.until(EC.element_to_be_clickable((by_type, identifier)))

    def skip_instructions(self):
        
        self.click_next_btn()
        self.click_next_btn()

        self.driver.find_elements_by_xpath("//*[contains(text(), 'Great')]")[0].click()

        self.wait_for_load("//*[contains(text(), 'Ok, got it')]")
        self.driver.find_elements_by_xpath("//*[contains(text(), 'Ok, got it')]")[0].click()
        
    def scrape_profile(self):
        scraped_imgs = []
        try:
            # Open profile
            self.wait_for_clickable(By.CLASS_NAME, 'recCard__openProfile')
            self.driver.find_elements_by_class_name('recCard__openProfile')[1].click()

            # Count number of profile pictures
            profile_card = self.driver.find_elements_by_class_name('profileCard__slider__backLink')[0]
            pic_elements = profile_card.find_elements_by_class_name('bullet')
            num_of_pictures = len(pic_elements) if len(pic_elements) != 0 else 1
            
            # Scrape images
            while len(scraped_imgs) < num_of_pictures:
                imgs = self.driver.find_elements_by_tag_name("img")
                for img in imgs:
                    img_src = img.get_attribute("src")
                    if "640x640" in img_src and img_src not in scraped_imgs:
                        scraped_imgs.append(img_src)

                # Next Photo
                self.driver.find_elements_by_class_name('pageButton')[1].click()
                
        except:
            print "Error scraping profile."

        finally:
            # Close profile
            self.driver.find_elements_by_class_name('profileCard__backArrow')[0].click()
            return scraped_imgs


    def dislike(self):
        self.driver.find_elements_by_class_name('recsGamepad__button--dislike')[0].click()
    

    def like(self):
        self.driver.find_elements_by_class_name('recsGamepad__button--like')[0].click()


    def connect(self):
        #self.phone_connect()
        self.fb_connect()
        self.skip_instructions()

        while True:
            scraped_imgs = self.scrape_profile()
            
            if len(scraped_imgs) == 0:
                continue

            print "profile pictures: "
            for img in scraped_imgs:
                print img

            ###########
            # Do something with images
            ###########
            x=5


    def start(self):
        self.connect()


t = Tinder(phone='+### #########', email="", password="")
t.start()