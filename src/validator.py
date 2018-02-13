"""
author: Bhavesh Motwani
Date : 2/12/2018

A validator file that contains methods to validate the correctness of required fields.
field_empty -> checks for empty fields.
check_date -> checks if a date is valid.
check_zipcode -> checks if a zipcode is valid.
check_amt -> check if a transaction amount is positive.
"""

from datetime import datetime

def field_empty(field):
	return field == ""

def check_date(date):
	try:
		datetime.strptime(date, "%m%d%Y")
		incorrectDate = False
	except ValueError:
		incorrectDate = True
	return len(date)!=8 or not all(e.isdigit() for e in date) or incorrectDate

def check_zipcode(zip_code):
	return len(zip_code)!=5 or not all(e.isdigit() for e in zip_code)

def check_amt(Transaction_AMT):
	return int(round(float(Transaction_AMT)))<0
