#!/usr/bin/python

# Amir Yazdanbakhsh
# a.yazdanbakhsh@gatech.edu

import json
import sys
from pprint import pprint

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main(argv):
    	
    if(len(argv) < 3):
    	print(bcolors.FAIL + "Usage: ./mnpu-scheduling.py <json file> <output file for scheduling>" + bcolors.ENDC)
    	exit(1)
    	pass

    # read JSON file
    with open(argv[1]) as data_file:    
    	data = json.load(data_file)

    #pprint(data)
    input_nodes  = str(data["input"])
    output_nodes = str(data["output"])
    hidden_layers = data["hidden"]

    print bcolors.OKGREEN + "%s" % input_nodes,
    for h in hidden_layers:
    	print "-> %s" % h["nodes"],
    	pass
    print "-> %s" % output_nodes,
    print bcolors.ENDC
    pass

if __name__ == "__main__":
    main(sys.argv)
