# functions para manipular as rows e visualizar data 
#!/usr/bin/python
import os
import sqlite3 as lite
import sys
import time

# na hora de passar a db, não esquecer da extensão!!! "nomedadb.db"
def showAllRowsSortedByDate(db):
    con = lite.connect(db)

def returnAllTablesFromDbAsList(db):
    con = lite.connect(db)
    all_tables = []
    with con:
        cur = con.cursor()
        res = con.execute("SELECT name from sqlite_master WHERE type='table';")
        for name in res:
            all_tables.append(name)

    if con: 
        con.close()
    return all_tables

def returnAllRowsOfCompanySortedByDate(db, table_name):
    con = lite.connect(db)
    rows_of_company_sorted = []
    with con:
        cur = con.cursor()
        # cur.execute("SELECT data, cotacao, minima, maxima, variacao, variacao_porcentagem, volume FROM " + table_name + " ORDER BY data DESC")
        cur.execute("SELECT * FROM " + table_name)
        
        sorted_company_data = cur.fetchall()
        rows_of_company_sorted = sorted_company_data
    if con:
        con.close()
    return rows_of_company_sorted

print(returnAllTablesFromDbAsList("stock_data.db"))
rows = returnAllRowsOfCompanySortedByDate("stock_data.db", "ADHM3_SA")
print(len(rows))
for i in rows:
    print(i)

# É POSSÍVEL QUE ESTEJA RETORNANDO DATA COMO ZERO PQ ESTA FAFZENDO DIVISAO?????