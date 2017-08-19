from selenium import webdriver
import selenium

import time

class pQuery():
    def __init__(self):
        print('pQuery class created')

    def xpath(self, drivere ,htmltag , htmlidentifier = 'empty', htmlidentname='empty', clicknum='not click'):

        def click(num=0):
            if type(self.elem) == list:
                self.elem[num].click()
            else:
                self.elem.click()

        boool = 1
        while boool:
            try:
                if htmlidentifier != 'empty':
                    elem = drivere.find_elements_by_xpath("//{0}[@{1}='{2}']".format(htmltag , htmlidentifier,
                                                                                     htmlidentname))
                else:
                    elem = drivere.find_elements_by_xpath("//{0}".format(htmltag))
                boool = 0
            except selenium.common.exceptions.NoSuchElementException as e:
                print(e)
        self.elem = elem

        if clicknum == 'not click':
            pass
        else:
            self.elem[clicknum].click()




driver = webdriver.Firefox()
URL = "file:///C:\\Users\\andre\\Desktop\\index.html"
driver.get(URL)
a = pQuery()
a.xpath(driver, 'span', 'class', 'calendarMonth')
# time.wait(4)
# elem = driver.find_element_by_name("login")
# elem.clear()
# elem.send_keys("andre.duarte/admin")