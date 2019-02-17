from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os

fmt = """>sample\nMAHHHHHHVDDDDKMAATAAAVVAEEDTELRDLLVQTLENSGVLNRIKAELRAAVFLALEEQEKVENIEGRKTPLVNESLMKFLNTKDGRLVASLVAEFLQFFNLDFTLAVFQPETSTLQGLEGRENLARDLGIIEAEGTVGGPLLLEVIRRW\n"""

chromedriver = '/Users/mac/webscript/chromedriver'

os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)

my_url = 'http://mbiljj45.bio.med.uni-muenchen.de:8888/prosoII/prosoII.seam'

driver.get(my_url)
driver.find_element_by_id("form1:inText").send_keys(fmt)
driver.find_element_by_id("form1:inText").send_keys(fmt)
driver.find_element_by_id("form1:j_id24").click()
wait = WebDriverWait(driver, 100)
element = wait.until(EC.invisibility_of_element_located((By.ID, "_viewRoot:status.start")))

page_soup = soup(driver.page_source, "html.parser")
tb = page_soup.findAll(id = "infoBlock_body")
slub = tb[0].findAll("td")
print(slub[2],slub[5])
print(slub[2].text)



"""for i in range(2):
	driver.find_element_by_id("form1:inText").send_keys(fmt)
	driver.find_element_by_id("form1:j_id24").click()
	wait = WebDriverWait(driver, 100)
	element = wait.until(EC.invisibility_of_element_located((By.ID, "_viewRoot:status.start")))
	page_soup = soup(driver.page_source, "html.parser")
	tb = page_soup.findAll("td")
	print("done!")

	driver.find_element_by_id("form1:inText").clear()"""

#driver.quit()


#containers = page_soup.findAll("h3", {"class": "LC20lb"})

#container = containers[0]

#print(type(container))
