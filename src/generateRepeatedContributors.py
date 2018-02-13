"""
author: Bhavesh Motwani
Date : 2/12/2018

Driver code that fetches itcont.txt and percentile.txt as input and 
provides repeat_donors as output.
"""

import sys
import time
from datetime import datetime
import bisect
import validator
import os

"""
funtion checks for empty or malformed fields,
Returns False for records with incorrect fields
"""
def checkFields(CMTE_ID,zip_Code,Name,Transaction_DT,Transaction_AMT,Other_ID):
	"""Set the flag to False when incorrect data is encountered"""
	flag = True
	"""Check if any of the required fields are empty and Other_ID is non-empty"""
	if(any(validator.field_empty(e) 
		for e in [CMTE_ID,zip_Code,Name,Transaction_DT,Transaction_AMT]) 
		or not validator.field_empty(Other_ID)):
		flag = False
	
	if(validator.check_date(Transaction_DT) or validator.check_zipcode(zip_Code)):
		flag = False
	"""Note: Please Comment the next two lines if negative donations are considered valid"""
	if(validator.check_amt(Transaction_AMT)):
		flag = False
	
	return flag

"""function to calculate the percentile from the file"""
def calculatePercentile(percentile_filename):
	return float(open(percentile_filename, "r").readline().strip())/100

"""Generates Repeated contibutors along with the number of repeated contributors,
	Total Transaction amount received from the repeated contributors,and Percentile
	after each repeated contribution for every CMTE_ID
	"""
def generateRepeatedContributors(input_filename, percentile ,output_filename):
	output = open(output_filename, "w")
	repeated_donors = set()
	donations = {}
	with open(input_filename,"r") as f:
		for line in f:
			fields = line.split("|")
			CMTE_ID, Name, zip_Code = fields[0], fields[7], fields[10][0:5]
			Transaction_DT, Transaction_AMT, Other_ID = fields[13], fields[14], fields[15]

			if(checkFields(CMTE_ID,zip_Code,Name,Transaction_DT,Transaction_AMT,Other_ID)):
				Transaction_DT = datetime.strptime(Transaction_DT, "%m%d%Y")
				year = Transaction_DT.year
				Transaction_AMT = int(round(float(Transaction_AMT)))
				if((Name + zip_Code) not in repeated_donors):
					repeated_donors.add((Name + zip_Code))
				else:
					if(CMTE_ID in donations):
						if ((year, zip_Code) in donations[CMTE_ID]):
							bisect.insort_right(donations[CMTE_ID][(year, zip_Code)], Transaction_AMT)
						else:
							donations[CMTE_ID][(year, zip_Code)] = [Transaction_AMT]
					else:
						donations[CMTE_ID] = {(year, zip_Code) : [Transaction_AMT]}
					length = len(donations[CMTE_ID][(year, zip_Code)])
					output.write("|".join([CMTE_ID, zip_Code, str(year),
											str(donations[CMTE_ID][(year, zip_Code)][int(round(length*percentile))-1]),
											str(sum(donations[CMTE_ID][(year, zip_Code)])),str(length)]))
					output.write("\n")				
	output.close()


if __name__ == "__main__":
	#input_filename = os.path.abspath("../input/itcont.txt")
	#percentile_file = os.path.abspath("../input/percentile.txt")
	#output_filename = os.path.abspath("../output/repeat_donors.txt")
	#generateRepeatedContributors(input_filename, calculatePercentile(percentile_file), output_filename)
	generateRepeatedContributors(sys.argv[1], calculatePercentile(sys.argv[2]), sys.argv[3])