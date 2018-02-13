"""
File to segment(divide) big input files into small chunks
for testing
python test.py number_of_lines -> generates two files.
1. itcont1.txt -> Input file with the specified number of lines.
2. output.txt -> file with the same number of lines where each line
				is followd by the last line number where a repeated donor
				was last seen.
"""


import sys

def filewrite(filename):
	f = open("output.txt","w")
	f2 = open("itcont1.txt","w")
	count = 0
	li = {}
	with open("itcont.txt","r") as fi:
		for index,line in enumerate(fi):
			if(count<int(filename)):
				fields = line.split("|")
				f.write("|".join([fields[0],fields[7],fields[10][0:5],
						fields[13],fields[14],fields[15]]))
				if((fields[7],fields[10][0:5]) in li):
					f.write("\t\t\t\t")
					f.write(str(li[(fields[7],fields[10][0:5])]))
				f.write("\n")
				li[(fields[7],fields[10][0:5])] = index+1
				count+=1
				f2.write(line)
			else:
				break
	f.close()
	f2.close()


if __name__ == "__main__":
	filewrite(sys.argv[1])