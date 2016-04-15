#!/usr/bin/python

# Amir Yazdanbakhsh
# Feb. 19 - 2016
# inputs: <line> <tpc> <sid> <log file> <output file>

import sys
import re

class dramRequest:
  subpart = -1
  chip = -1
  bank = -1
  row = -1
  col = -1
  burst = -1
  time = -1
pass


def main(argv):
	if(len(sys.argv) != 5):
		print("<tpc> <sid> <log file> <output file>")
		sys.exit(0)

	# extract inputs
	cid = sys.argv[1]
	sid = sys.argv[2]
	inputFile = sys.argv[3]
	outputFile = sys.argv[4]
	
	# read all lines
	lines = open(inputFile).readlines()
	regexPattern = r'time = ([0-9]+) [-] file = .* - line = ([0-9]+) [-] tpc = ([0-9]+) [-] sid = ([0-9]+) [-] wid = ([0-9]+) [-] pc = [0-9]+ [-] subpartition = ([0-9]+) [-] chip = ([0-9]+) [-] bank = ([0-9]+) [-] row = ([0-9]+) [-] col = ([0-9]+) [-] burst = ([0-9]+)'

	dramRequestDict = {}
	lineList = []
	for l in lines:
		l = l.rstrip()
		matchObj = re.match(regexPattern, l)
		if(matchObj):
			currTpc  = matchObj.group(3)
			currSid  = matchObj.group(4)
		pass
		if(matchObj and (int(currTpc) == int(cid)) and (int(currSid) == int(sid))):
			currTime = matchObj.group(1)
			currLine = matchObj.group(2)
			currWid  = matchObj.group(5)
			currSubPartition = matchObj.group(6)
			currChip = matchObj.group(7)
			currBank = matchObj.group(8)
			currRow = matchObj.group(9)
			currCol = matchObj.group(10)
			currBurst = matchObj.group(11)

			tempDramRequest = dramRequest()
			tempDramRequest.subpart = currSubPartition
			tempDramRequest.chip = currChip
			tempDramRequest.bank = currBank
			tempDramRequest.row = currRow
			tempDramRequest.col = currCol
			tempDramRequest.burst = currBurst
			tempDramRequest.time  = currTime

			dramRequestDict[(currWid,currLine)] = tempDramRequest
			if(currLine not in lineList):
				lineList.append(currLine)
			pass
		pass
	pass

	# write to file
	fout = open(outputFile, 'w')
	fout.write("time, wid, subpartition, chip, bank, row, col\n")
	fout.write("*"*10)
	fout.write("\n")
	for line in lineList:
		fout.write("---------------- line = %s ----------------\n" % (line))
		for i in range(32):
			if (str(i), str(line)) in dramRequestDict:
				fout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %
					      (	dramRequestDict[str(i), str(line)].time,
					      	i, # wid
					      	dramRequestDict[str(i), str(line)].subpart,
					       	dramRequestDict[str(i), str(line)].chip,
					       	dramRequestDict[str(i), str(line)].bank,
					       	dramRequestDict[str(i), str(line)].row,
					       	dramRequestDict[str(i), str(line)].col))
	pass
	fout.close()

if __name__ == "__main__":
    main(sys.argv[1:])