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
	#initialize evironment
	def __init__(self):
		print("Initializing PROSOII script...")
		self.n = 0

		#set up the SequenceMaker
		OrigSeq = '''MATKILALLALLALLVSATNAFIIPQCSLAPSASIPQFLPPVTSMGFEHPAVQAYRLQLALAASALQQPIAQLQQQSLAHLTLQTIATQQQQQQFLPSLSHLAVVNPVTYLQQQLLASNPLALANVAAYQQQQQLQQFMPVLSQLAMVNPAVYLQLLSSSPLAVGNAPTYLQQQLLQQIVPALTQLAVANPAAYLQQLLPFNQLAVSNSAAYLQQRQQLLNPLAVANPLVATFLQQQQQLLPYNQFSLMNPALQQPIVGGAIF'''
		self.SequenceMaker = SequenceMaker(OrigSeq)

		#initialize driver and preload the website
		chromedriver = '/Users/mac/webscript/chromedriver'
		os.environ["webdriver.chrome.driver"] = chromedriver
		self.driver = webdriver.Chrome(chromedriver)
		self.url = 'http://mbiljj45.bio.med.uni-muenchen.de:8888/prosoII/prosoII.seam'
		self.driver.get(self.url)
		print("Opening Browser...")

		#initialize database interface
		self.DbInterface = DbInterface('zeinsolub',\
		 									'proso')
		print("Initialized")

	#Begin scrapping 50 sequences input for n times
	#Unconstrained version
	def start_unconstrained(self, \
								n, length):
		print("Begin Mining...")
		for i in range(n):

			#Initialize data buffer
			data = []

			#Enter 50 random sequence into textarea
			for i in range(50):
				leng = random.randint(1,\
				 					length)
				randomSequence = self.SequenceMaker.generator_unconstrained(leng)
				self.driver.find_element_by_id("form1:inText")\
							.send_keys(">sample\n"+ randomSequence + "\n")
				aa_count_list, charge = self.SequenceMaker.count_aa_difference(randomSequence)
				data.append([False, 0, sum(aa_count_list), charge] + aa_count_list + [randomSequence])

			#Submmit text via Ajax
			self.driver.find_element_by_id("form1:j_id24").click()

			#Wait for data table to be loaded
			wait = WebDriverWait(self.driver, 1000000)
			element = wait.until(EC.invisibility_of_element_located((By.ID, "_viewRoot:status.start")))

			#Parsing raw HTML response and locate the result table
			page_soup = soup(self.driver.page_source, "html.parser")
			tb = page_soup.findAll(id = "infoBlock_body")
			slubs = tb[0].findAll("td")

			#Prepare data buffer to be written to database
			index = 0
			for i in range(2, 3*50, 3):
				temp = slubs[i].text.split(';')
				data[index][0] = True if temp[0] == 'soluble' else False
				data[index][1] = float(temp[1])
				index += 1

			#Upload data to database
			for item in data:
				print(item)
				self.DbInterface.insert(item)

			#Clear
			self.driver.find_element_by_id("form1:inText").clear()

		#close database session
		self.DbInterface.close_connection()
		self.n += n * 50
		print("Uploaded " + str(self.n) + " rows so far.")
