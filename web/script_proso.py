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
from database import DbInterface

class prosoWeb:
	"""interface of proso predictor"""
	def __init__(self):
		#set up the SequenceMaker
		OrigSeq = '''MATKILALLALLALLVSATNAFIIPQCSLAPSASIPQFLPPVTSMGFEHPAVQAYRLQLALAASALQQPIAQLQQQSLAHLTLQTIATQQQQQQFLPSLSHLAVVNPVTYLQQQLLASNPLALANVAAYQQQQQLQQFMPVLSQLAMVNPAVYLQLLSSSPLAVGNAPTYLQQQLLQQIVPALTQLAVANPAAYLQQLLPFNQLAVSNSAAYLQQRQQLLNPLAVANPLVATFLQQQQQLLPYNQFSLMNPALQQPIVGGAIF'''
		self.SequenceMaker = SequenceMaker(OrigSeq)
		#initialize driver and preload the website
		chromedriver = '/Users/mac/webscript/chromedriver'
		os.environ["webdriver.chrome.driver"] = chromedriver
		self.driver = webdriver.Chrome(chromedriver)
		self.url = 'http://mbiljj45.bio.med.uni-muenchen.de:8888/prosoII/prosoII.seam'
		self.driver.get(self.url)
		self.DbInterface = DbInterface('zeinsolub', 'proso')


	def start_unconstrained(self, n, length):
		for i in range(n):
			data = []
			for i in range(3):
				leng = random.randint(1, length)
				randomSequence = self.SequenceMaker.generator_unconstrained(leng)
				self.driver.find_element_by_id("form1:inText")\
							.send_keys(">sample\n"+ randomSequence + "\n")
				aa_count_list, charge = self.SequenceMaker.count_aa_difference(randomSequence)
				data.append([False, 0, sum(aa_count_list), charge] + aa_count_list + [randomSequence])
			self.driver.find_element_by_id("form1:j_id24").click()
			wait = WebDriverWait(self.driver, 100)
			element = wait.until(EC.invisibility_of_element_located((By.ID, "_viewRoot:status.start")))
			page_soup = soup(self.driver.page_source, "html.parser")
			tb = page_soup.findAll(id = "infoBlock_body")
			slubs = tb[0].findAll("td")

			index = 0
			for i in range(2, 3*3, 3):
				temp = slubs[i].text.split(';')
				data[index][0] = True if temp[0] == 'soluble' else False
				data[index][1] = float(temp[1])
				index += 1

			for item in data:
				self.DbInterface.insert(item)
			self.DbInterface.close_connection()



P = prosoWeb()
P.start_unconstrained(1, 10)
