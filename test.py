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

print (len(uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists("ITAU3.SA")))
print (type(uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists("ITAU3.SA")))

if 3>7:
	print("its true")

	print("still in?")
else:
	print ("false")