# To test situational stuff... can delete at any moment!
#!/usr/bin/python
import uol_scraper
import os
import requests
import bs4
import sqlite3 as lite
import sys
import time

## dd/mm/yyyy format
# print (time.strftime("%d/%m/%Y"))
# print ("HI " + time.strftime("%d"))
# print (time.strftime("%m"))
# print (time.strftime("%Y"))
def test():
	print (len(uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists("ITAU3.SA")))
	print (type(uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists("ITAU3.SA")))

	if 3>7:
		print("its true")

		print("still in?")
	else:
		print ("false")

def howToPrintDataFromTable(db, table):
	pass

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

def createTable(db, table_name):
	con = lite.connect(db)
	table_name = table_name.replace(".", "_")
	with con:
		cur = con.cursor()
		sqlite_command_drop = "DROP TABLE IF EXISTS "+ table_name
		sqlite_command_create = "CREATE TABLE "+ table_name +"(nome_jogo TEXT, volume_vendido REAL)"
		cur.execute(sqlite_command_drop)
		cur.execute(sqlite_command_create)
		print("Table " + table_name + " was created.")
	if con:
		con.close()

def makeSqliteDoSomething(db, table_name):
	con = lite.connect(db)
	with con:
		cur = con.cursor()
	if con:
		con.close()



createConnection("minha_bd.db")
createTable("minha_bd.db", "ALL_NINTENDO_GAMES")