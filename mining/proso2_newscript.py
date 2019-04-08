from new_database_interface import DbInterface
from squence_maker import SequenceMaker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re
import random
import os


class prosoWeb:
    """interface of proso predictor"""
    #	initialize evironment

    def __init__(self):
        print("Initializing PROSOII script...")
        self.n = 0

        #	set up the SequenceMaker
        OrigSeq = '''MATKILALLALLALLVSATNAFIIPQCSLAPSASIPQFLPPVTSMGFEHPAVQAYRLQLALAASALQQPIAQLQQQSLAHLTLQTIATQQQQQQFLPSLSHLAVVNPVTYLQQQLLASNPLALANVAAYQQQQQLQQFMPVLSQLAMVNPAVYLQLLSSSPLAVGNAPTYLQQQLLQQIVPALTQLAVANPAAYLQQLLPFNQLAVSNSAAYLQQRQQLLNPLAVANPLVATFLQQQQQLLPYNQFSLMNPALQQPIVGGAIF'''
        self.SequenceMaker = SequenceMaker(OrigSeq)

        #	initialize driver and preload the website
        chromedriver = '/Users/mac/webscript/chromedriver'
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        self.url = 'http://mbiljj45.bio.med.uni-muenchen.de:8888/prosoII/prosoII.seam'
        self.driver.get(self.url)
        print("Opening Browser...")

        #	initialize database interface
        self.DbInterface = DbInterface('zeinsolub',
                                       'proso2_new')
        print("Initialized")
        return

    #	Begin scrapping 5 sequences input for n times
    #	Unconstrained version
    def start_unconstrained_exact(self, startpoint):
        print("Begin unconstrained upto...")
        data = []
        count = 0
        with open("unc_exact50_sequence.fasta", "r") as se:
            for line in se:
                if count < startpoint:
                    count += 1
                else:
                    if not(line.startswith(">")):
                        randomSequence = line
                        self.driver.find_element_by_id("form1:inText")\
                            .send_keys(">sample" + str(count + 1) + "\n" + randomSequence + "\n")
                        data.append([count, False, 0, randomSequence])
                        count += 1
                        if count % 50 == 0:
                            self.driver.find_element_by_id(
                                "form1:j_id24").click()
                            wait = WebDriverWait(self.driver, 100000)
                            element = wait.until(EC.invisibility_of_element_located(
                                (By.ID, "_viewRoot:status.start")))
                            page_soup = soup(
                                self.driver.page_source, "html.parser")
                            tb = page_soup.findAll(id="infoBlock_body")
                            slubs = tb[0].findAll("td")
                            #	Prepare data buffer to be written to database
                            index = 0
                            for i in range(2, 3*50, 3):
                                temp = slubs[i].text.split(';')
                                data[index][1] = True if temp[0] == 'soluble' else False
                                data[index][2] = float(temp[1])
                                index += 1
                            #	Upload data to database
                            for item in data:
                                self.DbInterface.insert(item)
                                self.n += 1
                                print('---Written ' + str(self.n) + ' rows---')

                            #	Clear text area
                            self.driver.find_element_by_id(
                                "form1:inText").clear()
                            data = []
        return 0

    def start_unconstrained_upto(self):
        print("Begin unconstrained upto...")
        data = []
        count = 0
        with open("unc_upto50_sequence.fasta", "r") as se:
            for line in se:
                if not(line.startswith(">")):
                    randomSequence = line
                    self.driver.find_element_by_id("form1:inText")\
                        .send_keys(">sample" + str(count + 1) + "\n" + randomSequence + "\n")
                    data.append([count+1000, False, 0, randomSequence])
                    count += 1
                    if count % 50 == 0:
                        self.driver.find_element_by_id("form1:j_id24").click()
                        wait = WebDriverWait(self.driver, 100000)
                        element = wait.until(EC.invisibility_of_element_located(
                            (By.ID, "_viewRoot:status.start")))
                        page_soup = soup(
                            self.driver.page_source, "html.parser")
                        tb = page_soup.findAll(id="infoBlock_body")
                        slubs = tb[0].findAll("td")
                        #	Prepare data buffer to be written to database
                        index = 0
                        for i in range(2, 3*50, 3):
                            temp = slubs[i].text.split(';')
                            data[index][1] = True if temp[0] == 'soluble' else False
                            data[index][2] = float(temp[1])
                            index += 1
                        #	Upload data to database
                        for item in data:
                            self.DbInterface.insert(item)
                            self.n += 1
                            print('---Written ' + str(self.n) + ' rows---')

                        #	Clear text area
                        self.driver.find_element_by_id("form1:inText").clear()
                        data = []
        return 0

    def start_constrained_upto(self):
        print("Begin unconstrained upto...")
        data = []
        count = 0
        with open("c_upto50_sequence.fasta", "r") as se:
            for line in se:
                if not(line.startswith(">")):
                    randomSequence = line
                    self.driver.find_element_by_id("form1:inText")\
                        .send_keys(">sample" + str(count + 1) + "\n" + randomSequence + "\n")
                    data.append([count+2000, False, 0, randomSequence])
                    count += 1
                    if count % 50 == 0:
                        self.driver.find_element_by_id("form1:j_id24").click()
                        wait = WebDriverWait(self.driver, 100000)
                        element = wait.until(EC.invisibility_of_element_located(
                            (By.ID, "_viewRoot:status.start")))
                        page_soup = soup(
                            self.driver.page_source, "html.parser")
                        tb = page_soup.findAll(id="infoBlock_body")
                        slubs = tb[0].findAll("td")
                        #	Prepare data buffer to be written to database
                        index = 0
                        for i in range(2, 3*50, 3):
                            temp = slubs[i].text.split(';')
                            data[index][1] = True if temp[0] == 'soluble' else False
                            data[index][2] = float(temp[1])
                            index += 1
                        #	Upload data to database
                        for item in data:
                            self.DbInterface.insert(item)
                            self.n += 1
                            print('---Written ' + str(self.n) + ' rows---')

                        #	Clear text area
                        self.driver.find_element_by_id("form1:inText").clear()
                        data = []
        return 0

    def start_constrained_exact(self, startpoint):
        print("Begin unconstrained upto...")
        data = []
        count = 0
        with open("c_exact50_sequence.fasta", "r") as se:
            for line in se:
                if count < startpoint:
                    count += 1
                else:
                    if not(line.startswith(">")):
                        randomSequence = line
                        self.driver.find_element_by_id("form1:inText")\
                            .send_keys(">sample" + str(count + 1) + "\n" + randomSequence + "\n")
                        data.append([count+3000, False, 0, randomSequence])
                        count += 1
                        if count % 50 == 0:
                            self.driver.find_element_by_id(
                                "form1:j_id24").click()
                            wait = WebDriverWait(self.driver, 100000)
                            element = wait.until(EC.invisibility_of_element_located(
                                (By.ID, "_viewRoot:status.start")))
                            page_soup = soup(
                                self.driver.page_source, "html.parser")
                            tb = page_soup.findAll(id="infoBlock_body")
                            slubs = tb[0].findAll("td")
                            #	Prepare data buffer to be written to database
                            index = 0
                            for i in range(2, 3*50, 3):
                                temp = slubs[i].text.split(';')
                                data[index][1] = True if temp[0] == 'soluble' else False
                                data[index][2] = float(temp[1])
                                index += 1
                            #	Upload data to database
                            for item in data:
                                self.DbInterface.insert(item)
                                self.n += 1
                                print('---Written ' + str(self.n) + ' rows---')

                            #	Clear text area
                            self.driver.find_element_by_id(
                                "form1:inText").clear()
                            data = []
        return 0
