import uol_scraper
import os
import requests
import bs4
import sqlite3 as lite
import sys

# creates a respective table for the respective company in the db passed as argument
def createTable(db, table_name):
	con = lite.connect(db)
	table_name = table_name.replace(".", "_")
	with con:
		cur = con.cursor()
		sqlite_command_create = "CREATE TABLE "+ table_name +"(data TEXT, cotacao REAL, minima REAL, maxima REAL, variacao REAL, variacao_porcentagem REAL, volume INT)"
		sqlite_command_drop = "DROP TABLE IF EXISTS "+ table_name
		cur.execute(sqlite_command_drop)
		cur.execute(sqlite_command_create)
	if con:
		con.close()

# argument is one list with the 7 values we need for the company data
def insertIntoTable(connection_to_db, list_with_data, table_name):
	# con = lite.connect(db)
	table_name = table_name.replace(".", "_")
	with connection_to_db: 
		cur = connection_to_db.cursor()
		sqlite_command_insert = "INSERT INTO " + table_name + " VALUES(" + list_with_data[0]+","+list_with_data[1] + "," + list_with_data[2] + "," + list_with_data[3] + "," + list_with_data[4] + "," + list_with_data[5] + "," + list_with_data[6] +")"
		cur.execute(sqlite_command_insert)

# def insertStockDataIntoTable(data, cotacao, minima, maxima, variacao, variacao_porcentagem, volume, table):
	# pass

def handleDbInserting():
	pass

def main():
	# list_of_company_codes = returnCompanyCodesAsList()
		
	data = uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists("VIVR3.SA")
	for i in range(0,10):
		print(data[i])
	# for line in data:
	# 	if len(line) > 7:
	# 		print line

	test_list = ["VIVR3.SA"]

	for company in test_list:
		total_entries = 0
		createTable('stock_data.db', company)
		data = uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists(company)
		# maybe its faster putting the con here instead of inside the for loop? 
		con = lite.connect('stock_data.db')
		for line in data:
			# print "Inserting " + str(line) + " into table " + company
			insertIntoTable(con, line, company)
			total_entries+=1
			print(total_entries)
		# print("Total entries: " + total_entries)
		print("Sucessfully created and inserted data into table " + company)


main()

# todo now:
# 1) save the data from the tables to a table in the correct database.

# TA DANDO ERRO DO 12 VALUES WERE SUPPLIED POR CAUSA DAS BARRAS E DOS PONTOS NOS NUMEROS INSERIDOS! A TABELA PRECISA DE , PRA FLOAT E ACHO Q BARRAS TALVES SEJAM PROBLEMATICAS (?)
# PODE ESTAR MUITO DEVAGAR PORQUE ESTOU FECHANDO E ABRINDO A CONEXAO TODA VEZ!!!
# MAYBE ITS BETTER TO DO BULK INSERTS (MAYBE FASTER????)