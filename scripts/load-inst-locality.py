#!/usr/bin/python

# Amir Yazdanbakhsh
# Feb. 19 - 2016
# inputs: <approx line number> <log file> <output file>

import sys
import re
from sets import Set

# time = 43383 - file = _1.ptx - line = 251 - store = 1 - load = 0 - type = GLOBAL_ACC_W - size = 128 - mask = 01001000000000000000000001000010 - tpc = 2 - sid = 2 - wid = 10 - pc = 1160 - dwid = 42 - subpartition = 2 - chip = 1 - bank = 14 - row = 1378 - col = 256 - burst = 0

class dramRequest:
  subpart = -1
  chip = -1
  bank = -1
  row = -1
  col = -1
  time = -1
pass


def main(argv):
	if(len(sys.argv) != 4):
		print("<approx line number> <log file> <output file>")
		sys.exit(0)

	# extract inputs
	approxLoadFile = sys.argv[1]
	logFile = sys.argv[2]
	outputFile = sys.argv[3]

	# create approx list
	approxList = []
	for l in open(approxLoadFile).readlines():
		l = l.rstrip()
		approxList.append(l)
		pass	

	
	# read all lines
	lines = open(logFile).readlines()
	regexPattern = r'time = ([0-9]+) [-] file = .* - line = ([0-9]+) [-] store = ([0-9]+) [-] load = ([0-9]+) [-] type = .* [-] size = ([0-9]+) [-] mask = .* [-] tpc = ([0-9]+) [-] sid = ([0-9]+) [-] wid = ([0-9]+) [-] pc = [0-9]+ [-] dwid = ([0-9]+) [-] subpartition = ([0-9]+) [-] chip = ([0-9]+) [-] bank = ([0-9]+) [-] row = ([0-9]+) [-] col = ([0-9]+) [-] burst = ([0-9]+)'

	dramRequestDict = {}
	lineList = []
	similarReq = []
	for l in lines:
		l = l.rstrip()
		matchObj = re.match(regexPattern, l)
		currLine = 0
		if(matchObj):
			currLine  = matchObj.group(2)
		pass

		if(matchObj and (currLine in approxList)):

			currTIME = matchObj.group(1)
			currTPC  = matchObj.group(6)
			currSID  = matchObj.group(7)
			currDWID = matchObj.group(9)
			currSUBP = matchObj.group(10)
			currCHIP = matchObj.group(11)
			currBANK = matchObj.group(12)
			currROW  = matchObj.group(13)
			currCOL  = matchObj.group(14)

			# check if this row is already accessed
			# create a unique identifier
			UID = "%s-%s-%s" % (currTPC, currSID, currDWID)
			currKey = (UID,currLine)

			# use a set of requests for each line and warp
			# tempDramRequest = dramRequest()
			# tempDramRequest.subpart = currSUBP
			# tempDramRequest.chip    = currCHIP
			# tempDramRequest.bank 	= currBANK
			# tempDramRequest.row     = currROW
			# tempDramRequest.col     = currCOL
			# tempDramRequest.time    = currTIME
			if currKey not in dramRequestDict:
				dramRequestDict[currKey] = Set()
			dramRequestDict[currKey].add("%s-%s-%s-%s-%s" % (currLine, currSUBP, currCHIP, currBANK, currROW))

		pass
	pass

	# write to file
	print("Start writing...")
	fout = open(outputFile, 'w')
	fout.write("line, subpartition, chip, bank, row\n")
	fout.write("*"*10)
	fout.write("\n")
	for approxLine in approxList:
		fout.write("---------------- line = %s ----------------\n" % (approxLine))
		for k in dramRequestDict.iterkeys():
			if (k[1] == approxLine):
				currKey = (k[0],k[1])
				reqSet = dramRequestDict.get(currKey)
				fout.write("**** UID(TPC-SID-DWID) = %s ****\n" % k[0])
				for req in reqSet:
					fout.write("%s\n" % (req))
	pass
	fout.close()

if __name__ == "__main__":
    main(sys.argv[1:])