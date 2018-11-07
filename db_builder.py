# creates db, tables and updates tables
import os
import sys
import uol_scraper
import sqlite3 as lite

def createConnection(db_file):
    """ create a database connection to a SQLite database """
    # when you make a connection to an unexisting db, sqlite creates that db!
    try:
        conn = lite.connect(db_file)
        print(lite.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

# creates a respective table for the respective company in the db passed as argument
def createTable(db, table_name):
	con = lite.connect(db)
	table_name = table_name.replace(".", "_")
	with con:
		cur = con.cursor()
		sqlite_command_drop = "DROP TABLE IF EXISTS "+ table_name
		sqlite_command_create = "CREATE TABLE "+ table_name +"(data TEXT, cotacao REAL, minima REAL, maxima REAL, variacao REAL, variacao_porcentagem REAL, volume INT)"
		cur.execute(sqlite_command_drop)
		cur.execute(sqlite_command_create)
	if con:
		con.close()
		
# grabs the most recent day and start inserting newer historical quotation entries
def updateTable(db, table_name):
	pass

# argument is one list with the 7 values we need for the company data
# talvez seja melhor apenas passar o nome da db e criar o lite.connect(db) object dentro da função?
def insertIntoTable(connection_to_db, list_with_data, table_name):
	table_name = table_name.replace(".", "_")
	with connection_to_db: 
		cur = connection_to_db.cursor()
		sqlite_command_insert = "INSERT INTO " + table_name + " VALUES(" + list_with_data[0]+","+list_with_data[1] + "," + list_with_data[2] + "," + list_with_data[3] + "," + list_with_data[4] + "," + list_with_data[5] + "," + list_with_data[6] +")"
		cur.execute(sqlite_command_insert)

def main():
	# list_of_company_codes = returnCompanyCodesAsList()
	data = uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists("VIVR3.SA")
	# for i in range(0,len(uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists("VIVR3.SA"))):
		# print(str(i) + "________________" + str(data[i]))
	# for line in data:
	# 	if len(line) > 7:
	# 		print line

	list_of_companies_to_collect_data = ["LREN3.SA"]

	for company in list_of_companies_to_collect_data:
		total_entries = 0
		createTable('stock_data.db', company)
		data = uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists(company)

		if len(data) > 0:
			# maybe its faster putting the con here instead of inside the for loop? 
			con = lite.connect('stock_data.db')
			for line in data:
				# print "Inserting " + str(line) + " into table " + company
				insertIntoTable(con, line, company)
				total_entries+=1
				# print(total_entries)
			print("Total entries for " + company + ": " + str(total_entries))
			print("Sucessfully created and inserted data from " + company + " into table " + company.replace(".", "_"))
		
			if con:
				con.close()

		else:
			print ("No historical data to save. Did not create a DB for " + company)
main()

# todo now:
# pra atualizar apenas os dias que n estao na table, eh so pegar o ultimo dia
# na table e preparar a url com dia month e year begin e usar uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists