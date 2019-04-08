import os
import random
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from squence_maker import SequenceMaker
from new_database_interface import DbInterface


class ccsolWeb:
    """interface of proso predictor"""
    #	initialize evironment

    def __init__(self, url):
        print("Initializing PROSOII script...")
        self.n = 0

        #	set up the SequenceMaker
        OrigSeq = '''MATKILALLALLALLVSATNAFIIPQCSLAPSASIPQFLPPVTSMGFEHPAVQAYRLQLALAASALQQPIAQLQQQSLAHLTLQTIATQQQQQQFLPSLSHLAVVNPVTYLQQQLLASNPLALANVAAYQQQQQLQQFMPVLSQLAMVNPAVYLQLLSSSPLAVGNAPTYLQQQLLQQIVPALTQLAVANPAAYLQQLLPFNQLAVSNSAAYLQQRQQLLNPLAVANPLVATFLQQQQQLLPYNQFSLMNPALQQPIVGGAIF'''
        self.SequenceMaker = SequenceMaker(OrigSeq)

        #	initialize driver and preload the website
        chromedriver = '/Users/mac/webscript/chromedriver'
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        self.url = url
        self.driver.get(self.url)
        print("Opening Browser...")

        #	initialize database interface
        self.DbInterface = DbInterface('zeinsolub',
                                       'ccsol_new')
        print("Initialized")
        return

    def start(self, filename):
        data = []
        count = 0
        with open(filename, "r") as se:
            for line in se:
                if not(line.startswith(">")):
                    data.append([count+3000, False, 0, line])
                    count += 1
            page_soup = soup(self.driver.page_source, "html.parser")
            tb = page_soup.findAll(id="table")
            slubs = tb[0].findAll("td")
            #	Prepare data buffer to be written to database
            index = 0
            for i in range(2, 4*1000, 4):
                temp = slubs[i].text.split(';')
                data[index][1] = True if int(temp[0]) > 50 else False
                data[index][2] = float(temp[0])
                print(index, data[index])
                index += 1
            #	Upload data to database'''
            for item in data:
                self.DbInterface.insert(item)
                self.n += 1
                print('---Written ' + str(self.n) + ' rows---')
