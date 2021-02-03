#imports
import time
import sys
import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException  

def fetchWebsite(driver, address):
	# paper format dictionart
	paper = {'id': '', 'title': '', 'abstract': '', 'date': '', 'authors': [], 'references': [] }
	# fetch website
	driver.get(address)
	# respect hit rate
	time.sleep(2)
	# check if blocked
	# print(driver.page_source)
	try:
		# doi of paper
		path = "//body"
		# doi = wait.until(EC.visibility_of_element_located((By.XPATH, path))).get_attribute('originalurl')
		doi = driver.find_element_by_xpath(path).get_attribute('originalurl').split('/')[4]
		# print('doi found')
		paper['id'] = doi

		# title
		path = "//div[@class='name-section']/h1[@class='name']"
		# title = wait.until(EC.visibility_of_element_located((By.XPATH, path))).text
		title = driver.find_element_by_xpath(path).text
		# print('title found')
		paper['title'] = title

		# abstract
		path = "//div[@class='name-section']/p"
		# abstract = wait.until(EC.visibility_of_element_located((By.XPATH, path))).text
		abstract = driver.find_element_by_xpath(path).text
		# print('abstract found')
		paper['abstract'] = abstract

		# date published
		path = "//div[@class='name-section']/a[@class='au-target publication']/span[@class='year']"
		# date = wait.until(EC.visibility_of_element_located((By.XPATH, path))).text
		date = driver.find_element_by_xpath(path).text
		# print('date found')
		paper['date'] = date

		# authors list
		path = "//div[@class='name-section']/ma-author-string-collection/*/div[@class='authors']"
		# authorsList = wait.until(EC.visibility_of_element_located((By.XPATH, path)))
		authorsList = driver.find_element_by_xpath(path)
		# print('authorsList found')
		authors = []
		while(True):
			try:
				path = "div[" + str(len(authors) + 1) + "]/a[@class='au-target author link']"
				# author = WebDriverWait(authorsList, 10).until(EC.visibility_of_element_located((By.XPATH, path)))
				author = authorsList.find_element_by_xpath(path)
				# print(author.text)
				authors.append(author.text)
			except NoSuchElementException: # end of authors
				break
		paper['authors'] = authors

		# references list
		path = "//div[@class='ma-paper-results']/div[@class='results']"
		# refsList = wait.until(EC.visibility_of_element_located((By.XPATH, path)))
		refsList = driver.find_element_by_xpath(path)
		# print('refsList found')
		refs = []
		while(True and len(refs) < 10):
			try:
				path = "ma-card[" + str(len(refs) + 1) + "]/div/compose/div/div[@class='primary_paper']/a"
				# ref = WebDriverWait(refsList, 10).until(EC.visibility_of_element_located((By.XPATH, path)))
				ref = refsList.find_element_by_xpath(path)
				# print(ref.text)
				refs.append(ref.get_attribute('href').split('/')[4])
			except NoSuchElementException: # end of refs
				break
		paper['references'] = refs
	except NoSuchElementException:
		print('Error: ELEMENTS NOT FOUND! for paper ' + address.split('/')[4])
		paper['id'] = '0'
	return paper

def init():
	# firefox driver options
	opt = Options()
	opt.headless = True # hidden browser
	opt.add_argument('--disable-gpu') # disable graphics
	opt.add_argument("--window-size=1920,1200") # window size of the browser
	opt.add_argument("user-agent=Three Musketeers") # change user agent
	opt.add_argument('log-level=3') # only log fatal errors
	# set the web driver
	driver = webdriver.Firefox(options=opt, executable_path='drivers/firefoxdriver.exe')
	return driver

def reptile(starter, LIMIT):
	# get crawling queue
	queue = []
	with open(starter, 'r', encoding = 'utf-8') as f:
		lines = f.readlines()
		for l in lines:
			queue.append(l[0:-1].split('/')[4])
		f.close()
	count = len(queue)
	# print(queue)

	# initialize driver
	driver = init()
	print('\n******** Crawling Initiated ********\n')

	# create database crawling list
	db = []
	fetchedPapers = []

	# crawling loop
	while len(fetchedPapers) < LIMIT:
		id = queue[0] # first paper of the queue
		queue = queue[1:] # update queue
		if id in fetchedPapers: # fetched before
			continue
		# new paper
		address = "https://academic.microsoft.com/paper/" + id # convert paper id to url
		paper = fetchWebsite(driver, address) # fetch website
		print('{}\t{}\tfetched'.format(len(fetchedPapers),id))
		if(paper['id'] == '0'): # unsuccessful fetch
			continue
		db.append(paper) # add paper to the database
		fetchedPapers.append(id) # just fetched
		# add references to the queue
		for ref in paper['references']:
			queue.append(ref)
	# terminate the driver
	driver.quit()
	print('\n******** Crawling Terminated ********\n')
	# save database to local file
	with open('database-firefox.json', 'w', encoding = 'utf-8') as f:
		json.dump(db, f)
		f.close

def usage():
	print('usage: python3 Crawler-Firefox.py LIMIT')
	sys.exit(2)

def main():
	if len(sys.argv) != 2:
		usage()
	LIMIT = int(sys.argv[1])
	# run the crawler
	reptile('start.txt', LIMIT)

if __name__=='__main__':
	main()
