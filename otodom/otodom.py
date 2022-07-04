from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import otodom.constants as const


class Otodom(webdriver.Chrome):
    def __init__(self,teardown=False):
        super(Otodom,self).__init__()
        self.teardown=teardown
        self.implicitly_wait(15)
        self.maximize_window()
    
    def openPage(self):

        #Loads page defined in constants, clicks the cookies popup and navigates to the apartments page
        self.get(const.BASE_URL)
        self.find_element_by_id("onetrust-accept-btn-handler").click()
        self.find_element_by_id("frontend.navbar.menu.ads").click()
        self.find_element_by_id("frontend.navbar.menu.ads-frontend.navbar.menu.ads.apartments-for-sale").click()

        #Waits for the features popup to appear and clicks it
        popup = WebDriverWait(self, 8).until(EC.element_to_be_clickable((By.CLASS_NAME,'css-jjrhw1')))
        popup.click()
    
    def search(self,city):
 
        #Iputs and searchers for the provided city,
        #navigates trough the fields choosing only second hand market
        self.find_element_by_id('location').click()
        self.find_element_by_id('location-picker-input').send_keys(city)
        time.sleep(1)
        self.find_element_by_xpath(
        '//div[@id="__next"]/div/main/div/div[2]/div/form/div/div[3]/div/div/div[2]/ul/li').click()
        time.sleep(1)
        self.find_element_by_xpath('//label').click()
        time.sleep(1)
        self.find_element_by_xpath('//div[2]/div/div/div/div/div/div[2]/div').click()
        time.sleep(1)
        self.find_element_by_xpath('//div[2]/div/div[3]/div').click()
        time.sleep(1)
        self.find_element_by_id('search-form-submit').click()
        time.sleep(2)

    def scrape(self):

        #Scrapes all of the offer pages for the price and size of the apartments
        #Calculates the average price, reutrns the value and the number of offers processed
        
        pages=self.find_elements_by_class_name('eoupkm71') #
        nextPages=(int(pages[len(pages)-3].text))          #Getting the number of pages to scrape

        offerList=[]
        while nextPages>=0:

            nonPromoted = self.find_elements(By.CLASS_NAME,'css-14cy79a')[1]      #Picking up just the non promoted offers
            for offer in nonPromoted.find_elements(By.CLASS_NAME,'css-i38lnz'):   #Getting the required data in tex for on a list
                offerList.append(offer.text)
            time.sleep(2)

            self.find_element(By.XPATH,'//button[@data-cy="pagination.next-page"]').click() #Going to the next page

            nextPages-=1


        #Processes the offers the get the integer value of price per square meter
        avgPrice=0
        for offer in offerList:
            avgPrice+=int(offer[(offer.index('\n')+1):(offer.find(' ',(offer.index('\n'))+3))]) 
        avgPrice=avgPrice/len(offerList)
       
        self.quit()
        return [len(offerList),round(avgPrice)]


