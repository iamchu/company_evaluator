# handles scraping a list of all companies quoted in brazils stock market (Bovespa)
# also handles the scraping of their individual historical quotations.
# the saving and db managing will be made in another file
# talvez usar http://www.bmfbovespa.com.br/pt_br/servicos/market-data/historico/mercado-a-vista/series-historicas/ para dados historicos
import os
import sys
import bs4
import time
import requests
import sqlite3 as lite

# grab BOVESPA company codes from 
def returnCompanyCodesAsList():
	url = 'https://cotacoes.economia.uol.com.br/acoes-bovespa.html?exchangeCode=.BVSP&page=1&size=10000'
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

def scrapeCompanyQuotationsAndReturnAsListOfLists(company_code):
	url = 'https://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html?codigo=' + company_code + '&beginDay=01&beginMonth=01&beginYear=2000&endDay='+ time.strftime("%d") +'&endMonth='+ time.strftime("%m") + '&endYear='+time.strftime("%Y")+'&page=1&size=10000'

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

	# if the company code goes to a page with no historical data (no quotations), this list is empty. It has len(company_historical_data) = 0
	return company_historical_data