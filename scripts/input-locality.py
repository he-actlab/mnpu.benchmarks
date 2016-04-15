#!/usr/bin/python

# Amir Yazdanbakhsh
# March. 10 - 2016
# inputs: <input lines file> <stat file>

import sys
import re
from sets import Set



def main(argv):
	if(len(sys.argv) != 3):
		print("<input lines file> <stat file>")
		sys.exit(0)

	# extract inputs
	inputLineFile = sys.argv[1]
	statFile = sys.argv[2]

	# create approx list
	inputLines = []
	for l in open(inputLineFile).readlines():
		l = l.rstrip()
		inputLines.append(l)
	pass	

	uidDict = {}
	regexPattern = r'.*UID\(TPC-SID-DWID\) = ([0-9]+)[-]([0-9]+)[-]([0-9]+) .*'
	requestPattern = r'([0-9]+)[-]([0-9]+)[-]([0-9]+)[-]([0-9]+)[-]([0-9]+)'
	# read all the stat files
	statLines = open(statFile).readlines()
	for l in statLines:
		l = l.rstrip()
		matchObj = re.match(regexPattern, l)
		if(matchObj):
			uidDict["%s-%s-%s" % (matchObj.group(1), matchObj.group(2), matchObj.group(3))] = Set()
	pass


	isDone = False
	for i in range(len(statLines)):
		l = statLines[i].rstrip()
		matchObj = re.match(regexPattern, l)
		if(isDone):
			break
		if(matchObj):
			for j in range(i+1, len(statLines)):
				reqL = statLines[j].rstrip()
				matchReq = re.match(requestPattern, reqL)
				if ("*" in reqL) or ("line =" in reqL):
					break
				if(matchReq.group(1) not in inputLines): # if line number is not in the input lines break
					break
					isDone = True
				uidDict["%s-%s-%s" % (matchObj.group(1), matchObj.group(2), matchObj.group(3))].add("%s-%s" % (matchReq.group(2), matchReq.group(3)))
			pass
	pass


	
	#print("%s: %d" % (k, len(uidDict[k])))
	print float(sum(len(d) for d in uidDict.values())) / len(uidDict) / len(inputLines)



	# # read all lines
	# lines = open(logFile).readlines()
	# regexPattern = r'time = ([0-9]+) [-] file = .* - line = ([0-9]+) [-] store = ([0-9]+) [-] load = ([0-9]+) [-] type = .* [-] size = ([0-9]+) [-] mask = .* [-] tpc = ([0-9]+) [-] sid = ([0-9]+) [-] wid = ([0-9]+) [-] pc = [0-9]+ [-] dwid = ([0-9]+) [-] subpartition = ([0-9]+) [-] chip = ([0-9]+) [-] bank = ([0-9]+) [-] row = ([0-9]+) [-] col = ([0-9]+) [-] burst = ([0-9]+)'

	# dramRequestDict = {}
	# lineList = []
	# similarReq = []
	# for l in lines:
	# 	l = l.rstrip()
	# 	matchObj = re.match(regexPattern, l)
	# 	currLine = 0
	# 	if(matchObj):
	# 		currLine  = matchObj.group(2)
	# 	pass

	# 	if(matchObj and (currLine in approxList)):

	# 		currTIME = matchObj.group(1)
	# 		currTPC  = matchObj.group(6)
	# 		currSID  = matchObj.group(7)
	# 		currDWID = matchObj.group(9)
	# 		currSUBP = matchObj.group(10)
	# 		currCHIP = matchObj.group(11)
	# 		currBANK = matchObj.group(12)
	# 		currROW  = matchObj.group(13)
	# 		currCOL  = matchObj.group(14)

	# 		# check if this row is already accessed
	# 		# create a unique identifier
	# 		UID = "%s-%s-%s" % (currTPC, currSID, currDWID)
	# 		currKey = (UID,currLine)

	# 		# use a set of requests for each line and warp
	# 		# tempDramRequest = dramRequest()
	# 		# tempDramRequest.subpart = currSUBP
	# 		# tempDramRequest.chip    = currCHIP
	# 		# tempDramRequest.bank 	= currBANK
	# 		# tempDramRequest.row     = currROW
	# 		# tempDramRequest.col     = currCOL
	# 		# tempDramRequest.time    = currTIME
	# 		if currKey not in dramRequestDict:
	# 			dramRequestDict[currKey] = Set()
	# 		dramRequestDict[currKey].add("%s-%s-%s-%s-%s" % (currLine, currSUBP, currCHIP, currBANK, currROW))

	# 	pass
	# pass

	# # write to file
	# print("Start writing...")
	# fout = open(outputFile, 'w')
	# fout.write("line, subpartition, chip, bank, row\n")
	# fout.write("*"*10)
	# fout.write("\n")
	# for approxLine in approxList:
	# 	fout.write("---------------- line = %s ----------------\n" % (approxLine))
	# 	for k in dramRequestDict.iterkeys():
	# 		if (k[1] == approxLine):
	# 			currKey = (k[0],k[1])
	# 			reqSet = dramRequestDict.get(currKey)
	# 			fout.write("**** UID(TPC-SID-DWID) = %s ****\n" % k[0])
	# 			for req in reqSet:
	# 				fout.write("%s\n" % (req))
	# pass
	# fout.close()

if __name__ == "__main__":
    main(sys.argv[1:])