# handles scraping a list of all companies quoted in brazils stock market (Bovespa)
# also handles the scraping of their individual historical quotations.
# the saving and db managing will be made in another file

import os
import requests
import bs4
import sqlite3 as lite
import sys

# grab BOVESPA company codes
def returnCompanyCodesAsList():
	url = 'https://cotacoes.economia.uol.com.br/acoes-bovespa.html?exchangeCode=.BVSP&page=1&size=3000'
	list_of_company_codes = []
	total_of_companies = 0

	page = requests.get(url)
	page.raise_for_status()

	cotacoes_soup = bs4.BeautifulSoup(page.text, "lxml")
	bs4_company_codes = cotacoes_soup.find_all(class_ = "clear-box")

	for line in bs4_company_codes:
		this_company_code_soup = bs4.BeautifulSoup(str(line), "lxml")
		if len(this_company_code_soup.find_all('span')) > 1:
			# print this_company_code_soup.find_all('span')[1].get_text()
			list_of_company_codes.append(this_company_code_soup.find_all('span')[1].get_text())
			total_of_companies+=1

	print('Total of ' + str(total_of_companies) + ' companies listed in BOVESPA (Note that some may be deprecated)')
	return list_of_company_codes

# populate db with data from url passed as argument
def scrapeCompanyQuotationsAndReturnAsListOfLists(company_code):
	url = 'https://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html?codigo=' + company_code + '&beginDay=1&beginMonth=1&beginYear=2004&endDay=1&endMonth=1&endYear=2018&page=1&size=10000'

	page = requests.get(url)
	page.raise_for_status()
	# grab the lines as items on a list
	# go through each of the items and break in a sublist and grab the corresponding items accordingly

	soup = bs4.BeautifulSoup(page.text, "lxml")
	tblInterday = soup.find(id="tblInterday")	
	soup = bs4.BeautifulSoup(str(tblInterday), "lxml")	

	lines = soup.find_all("tr")
	company_historical_data = []

	# Here the range starts at 1 because the tblInterday has headers
	for i in range(1,len(lines)):
		# holds the data for one line of the historical quotations table. This is so we can append to the company_historical_data
		current_line_historical_data = []
		line_soup = bs4.BeautifulSoup(str(lines[i]), "lxml")

		line_values = line_soup.find_all("td")

		for j in range(len(line_values)):
			if j < 6:
				current_line_historical_data.append(line_values[j].get_text().replace(",", "."))
			else:
				current_line_historical_data.append(line_values[j].get_text().replace(".", ""))
		company_historical_data.append(current_line_historical_data)

	return company_historical_data