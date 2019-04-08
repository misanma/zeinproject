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
from database_interface import DbInterface


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
        self.url = 'http://mbiljj45.bio.med.uni-muenchen.de:8888/proso/proso.seam'
        self.driver.get(self.url)
        print("Opening Browser...")

        #	initialize database interface
        self.DbInterface = DbInterface('zeinsolub',
                                       'proso1')
        print("Initialized")
        return

    def generate_file_unconstrained_upto(self, n, length):
        with open("unc_upto"+str(length)+"_sequence.fasta", "w") as se:
            for i in range(n):
                leng = random.randint(1,
                                      length)
                randomSequence = self.SequenceMaker.generator_unconstrained(
                    leng)
                se.write(">sample" + str(i) + "\n")
                se.write(randomSequence + "\n")

    def generate_file_unconstrained_exact(self, n, length):
        with open("unc_exact"+str(length)+"_sequence.fasta", "w") as se:
            for i in range(n):
                leng = length
                randomSequence = self.SequenceMaker.generator_unconstrained(
                    leng)
                se.write(">sample" + str(i) + "\n")
                se.write(randomSequence + "\n")

    def generate_file_constrained_upto(self, n, length):
        with open("c_upto"+str(length)+"_sequence.fasta", "w") as se:
            for i in range(n):
                leng = random.randint(1,
                                      length)
                randomSequence = self.SequenceMaker.generator_constrained(
                    leng, -2, 2)
                se.write(">sample" + str(i) + "\n")
                se.write(randomSequence + "\n")

    def generate_file_constrained_exact(self, n, length):
        with open("c_exact"+str(length)+"_sequence.fasta", "w") as se:
            for i in range(n):
                leng = length
                randomSequence = self.SequenceMaker.generator_constrained(
                    leng, -2, 2)
                se.write(">sample" + str(i) + "\n")
                se.write(randomSequence + "\n")

    #	Begin scrapping 5 sequences input for n times
    #	Unconstrained version

    def start_unconstrained_upto(self,
                                 n, length):
        print("Begin Mining...")
        for i in range(n):

            #	Initialize data buffer
            data = []

            #	Enter 5 random sequence into textarea
            for i in range(5):
                leng = random.randint(1,
                                      length)
                randomSequence = self.SequenceMaker.generator_unconstrained(
                    leng)
                self.driver.find_element_by_id("form1:inText")\
                    .send_keys(">sample\n" + randomSequence + "\n")
                aa_count_list, charge = self.SequenceMaker.count_aa_difference(
                    randomSequence)
                data.append([False, 0, sum(aa_count_list), charge] +
                            aa_count_list + [randomSequence])

            #	Submmit text via Ajax
            self.driver.find_element_by_id("form1:j_id24").click()

            #	Wait for data table to be loaded
            wait = WebDriverWait(self.driver, 100000)
            element = wait.until(EC.invisibility_of_element_located(
                (By.ID, "_viewRoot:status.start")))

            #	Parsing raw HTML response and locate the result table
            page_soup = soup(self.driver.page_source, "html.parser")
            tb = page_soup.findAll(id="infoBlock_body")
            slubs = tb[0].findAll("td")

            #	Prepare data buffer to be written to database
            index = 0
            for i in range(2, 3*5, 3):
                temp = slubs[i].text.split(';')
                data[index][0] = True if temp[0] == 'yes' else False
                data[index][1] = float(temp[1])
                index += 1

            #	Upload data to database
            for item in data:
                self.DbInterface.insert(item)
                self.n += 1
                print('---Written ' + str(self.n) + ' rows---')

            #	Clear text area
            self.driver.find_element_by_id("form1:inText").clear()
        return 0

    #	Begin scrapping 5 sequences input for n times with constrained charge
    #	Unconstrained version
    def start_constrained_fixed(self, n, length, positive, negative):
        print("Begin Mining...")
        for i in range(n):

            #	Initialize data buffer
            data = []

            #	Enter 5 random sequence into textarea
            for i in range(5):
                leng = length
                charge = total_sub = -1
                #		make sure the sequence fits the reqirement
                while not(charge >= (5 - negative) and charge <= (5 + positive) and total_sub == leng):
                    randomSequence = self.SequenceMaker.generator_constrained(
                        leng, -negative, positive)
                    aa_count_list, charge = self.SequenceMaker.count_aa_difference(
                        randomSequence)
                    total_sub = sum(aa_count_list)
                #	Input to text area
                self.driver.find_element_by_id("form1:inText")\
                    .send_keys(">sample\n" + randomSequence + "\n")

                #	write to buffer
                data.append([False, 0, sum(aa_count_list), charge] +
                            aa_count_list + [randomSequence])

            #	Submmit text via Ajax
            self.driver.find_element_by_id("form1:j_id24").click()

            #	Wait for data table to be loaded
            wait = WebDriverWait(self.driver, 100000)
            element = wait.until(EC.invisibility_of_element_located(
                (By.ID, "_viewRoot:status.start")))

            #	Parsing raw HTML response and locate the result table
            page_soup = soup(self.driver.page_source, "html.parser")
            tb = page_soup.findAll(id="infoBlock_body")
            slubs = tb[0].findAll("td")

            #	Prepare data buffer to be written to database
            index = 0
            for i in range(2, 3*5, 3):
                temp = slubs[i].text.split(';')
                data[index][0] = True if temp[0] == 'soluble' else False
                data[index][1] = float(temp[1])
                index += 1

            #	Upload data to database
            for item in data:
                self.DbInterface.insert(item)
                self.n += 1
                print('---Written ' + str(self.n) + ' rows---')

            #	Clear text area
            self.driver.find_element_by_id("form1:inText").clear()
        return 0

    #	Begin scrapping 5 sequences input for n times
    #	Unconstrained version
    def start_unconstrained_fixed(self,
                                  n, length):
        print("Begin Mining...")
        for i in range(n):

            #	Initialize data buffer
            data = []

            #	Enter 5 random sequence into textarea
            for i in range(5):
                leng = length
                randomSequence = self.SequenceMaker.generator_unconstrained(
                    leng)
                self.driver.find_element_by_id("form1:inText")\
                    .send_keys(">sample\n" + randomSequence + "\n")
                aa_count_list, charge = self.SequenceMaker.count_aa_difference(
                    randomSequence)
                data.append([False, 0, sum(aa_count_list), charge] +
                            aa_count_list + [randomSequence])

            #	Submmit text via Ajax
            self.driver.find_element_by_id("form1:j_id24").click()

            #	Wait for data table to be loaded
            wait = WebDriverWait(self.driver, 100000)
            element = wait.until(EC.invisibility_of_element_located(
                (By.ID, "_viewRoot:status.start")))

            #	Parsing raw HTML response and locate the result table
            page_soup = soup(self.driver.page_source, "html.parser")
            tb = page_soup.findAll(id="infoBlock_body")
            slubs = tb[0].findAll("td")

            #	Prepare data buffer to be written to database
            index = 0
            for i in range(2, 3*5, 3):
                temp = slubs[i].text.split(';')
                data[index][0] = True if temp[0] == 'yes' else False
                data[index][1] = float(temp[1])
                index += 1

            #	Upload data to database
            for item in data:
                self.DbInterface.insert(item)
                self.n += 1
                print('---Written ' + str(self.n) + ' rows---')

            #	Clear text area
            self.driver.find_element_by_id("form1:inText").clear()
        return 0

    #	Begin scrapping 5 sequences input for n times with constrained charge
    #	Unconstrained version

    def start_constrained_upto(self, n, length, positive, negative):
        print("Begin Mining...")
        for i in range(n):

            #	Initialize data buffer
            data = []

            #	Enter 5 random sequence into textarea
            for i in range(5):
                leng = random.randint(1,
                                      length)
                charge = total_sub = -1
                #		make sure the sequence fits the reqirement
                while not(charge >= (5 - negative) and charge <= (5 + positive) and total_sub == leng):
                    randomSequence = self.SequenceMaker.generator_constrained(
                        leng, -negative, positive)
                    aa_count_list, charge = self.SequenceMaker.count_aa_difference(
                        randomSequence)
                    total_sub = sum(aa_count_list)
                #	Input to text area
                self.driver.find_element_by_id("form1:inText")\
                    .send_keys(">sample\n" + randomSequence + "\n")

                #	write to buffer
                data.append([False, 0, sum(aa_count_list), charge] +
                            aa_count_list + [randomSequence])

            #	Submmit text via Ajax
            self.driver.find_element_by_id("form1:j_id24").click()

            #	Wait for data table to be loaded
            wait = WebDriverWait(self.driver, 100000)
            element = wait.until(EC.invisibility_of_element_located(
                (By.ID, "_viewRoot:status.start")))

            #	Parsing raw HTML response and locate the result table
            page_soup = soup(self.driver.page_source, "html.parser")
            tb = page_soup.findAll(id="infoBlock_body")
            slubs = tb[0].findAll("td")

            #	Prepare data buffer to be written to database
            index = 0
            for i in range(2, 3*5, 3):
                temp = slubs[i].text.split(';')
                data[index][0] = True if temp[0] == 'soluble' else False
                data[index][1] = float(temp[1])
                index += 1

            #	Upload data to database
            for item in data:
                self.DbInterface.insert(item)
                self.n += 1
                print('---Written ' + str(self.n) + ' rows---')

            #	Clear text area
            self.driver.find_element_by_id("form1:inText").clear()
        return 0
