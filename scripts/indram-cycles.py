#!/bin/usr/python

# Amir Yazdanbakhsh
# Apr. 14, 2016

import os
import json
import sys
import subprocess
from pprint import pprint
from enum import Enum

# bank state enum
class bank_state(Enum):
	idle = 0
	active = 1
pass

# bank last command
class bank_rw(Enum):
	read = 0
	write = 1
pass


# neural network configuration
class neural_network(object):
	def __init__(self, input_neurons, hidden_layers_list, output_neurons):
		self.input_neurons = input_neurons
		self.hidden_layers_list = hidden_layers_list
		self.output_neurons = output_neurons
	pass
	def n_input_neurons(self):
		return int(self.input_neurons)
	pass
	def n_output_neurons(self):
		return int(self.output_neurons)
	pass
	def n_hidden_layers(self):
		return len(self.hidden_layers_list)
	pass
	def n_hidden_all_neurons(self):
		return hidden_layers_list
	pass
	def n_hidden_neurons(self, l):
		return int(self.hidden_layers_list[l])
	pass
pass

######################### Start of timing constraint #########################
# BANK - BANKGROUP - CHIP level timing constraints
# Note: we might need to add some timing for temporary storage
# bank timing
class bank_timing(object):
	def __init__(self, tRCD, tWL, tRAS, tRP, tRC, tWTP, tRTP, bg_idx):
		# ACTIVATE to READ/WRITE
		self.tRCD = tRCD
		# WRITE Latency
		self.tWL  = tWL
		# ACTIVATE to WRITE command (why? from GPGPU-Sim)
		self.tRCDWR = self.tRCD - (self.tWL + 1)
		# ACTIVATE to PRECHARGE
		self.tRAS = tRAS
		# ROW PRECHARGE to ACTIVATE
		self.tRP = tRP
		# ACTIVATE to ACTIVATE same bank
		self.tRC = tRC
		# WRITE to PRECHARGE same bank
		self.tWTP = tWTP
		# READ to PRECHARGE same bank
		self.tRTP = tRTP
		# bankgroup index
		self.bg_idx = bg_idx

		# idle/active
		self.state = bank_state.idle
		# READ/WRITE
		self.rw = bank_rw.read
		# current row (initialized to no row)
		self.curr_row = -1

		# stats
		self.n_accesses = 0
		self.n_writes = 0
		self.n_reads = 0
		self.n_idle = 0
	pass
pass
# bankgroup timing
class bankgroup_timing(object):
	def __init__(self, tCCDL, tRTPL):
		# WRITE/READ to WRITE/READ same bankgroup
		self.tCCDL = tCCDL
		# READ to PRECHARGE same bankgroup
		self.tRTPL = tRTPL
	pass
pass
#chip timing
class chip_timing(object):
	def __init__(self, tRRD, tCCD, tRTW, tWTR):
		# ACTIVATE to ACTIVATE command different banks
		self.tRRD = tRRD
		# WRITE/READ to WRITE/READ different bankgroup
		self.tCCD = tCCD
		# READ to WRITE delay
		self.tRTW = tRTW
		# WRITE to READ delay (same or different bankgroup)
		self.tWTR = tWTR
	pass
pass
######################### End of timing constraint #########################

######################### Start of DRAM structure #########################
# DRAM bank
class bank(object):
	def __init__(self, idx, row, col, buff_size, tBank):
		self.idx = idx
		self.row = row
		self.col = col
		self.buff_size = buff_size
		self.tBank = tBank
	pass
pass
# DRAM bankgroup
class bankgroup(object):
	def _init__(self, idx, tBankgroup):
		self.idx = idx
		self.bank_array = []
		self.tBankgroup = tBankgroup
	pass
	def add_bank(self, b):
		self.bank_array.append(b)
	pass
pass

class dram_chip(object):
	def _init__(self, idx, tDram):
		self.idx = idx
		self.bankgroup_array = []
		self.tDram = tDram
	pass
	def add_bankgroup(self, bg):
		self.bankgroup_array.append(bg)
	pass
pass
######################### End of DRAM structure #########################

configs=json.loads(open('system-config.json').read())


# neural network topology
input_neurons  = configs["accl"]["input"]
hidden_layers_list = configs["accl"]["hidden"]
output_neurons = configs["accl"]["output"]

curr_nn = neural_network(input_neurons, hidden_layers_list, output_neurons)
print(curr_nn.n_input_neurons())
print(curr_nn.n_output_neurons())
print(curr_nn.n_hidden_neurons(0))
print(curr_nn.n_hidden_neurons(1))
