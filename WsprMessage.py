#!/usr/bin/env python3

import string

class WsprMessage:

	syncVector = [1,1,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,1,0,1,1,1,1,0,0,0,0,
				  0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,1,1,0,
				  1,0,0,0,0,1,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1,0,1,1,0,0,0,1,1,0,1,
				  0,1,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,1,1,0,1,0,0,
				  0,1,1,1,0,0,0,0,0,1,0,1,0,0,1,1,0,0,0,0,0,0,0,1,1,0,1,0,1,1,0,
				  0,0,1,1,0,0,0]

	def __init__(self,call,loc,pwr):
		self.callstr = call.upper()
		self.locstr = loc.upper()
		self.pwr = pwr
		self.chanSym = []

		if len(self.callstr) > 6:
			print("Invalid callsign!")
		if len(self.locstr) > 4:
			print("Invalid locator!")
		if self.pwr not in range(0,61):
			print("Invalid power!")

	def setCall(self,call):
		self.callstr = call

	def setLocator(self,loc):
		self.locstr = loc

	def setPower(self,pwr):
		self.pwr = pwr

	# generates the channel symbols needed to transmit the WSPR message passed
	# in the constructor
	def channelSymbols(self):
		ecall = self.encodeCallsign()
		eloc = self.encodeLocator()
		convmsg = self.convoCode(ecall,eloc)
		imsg = self.interleave(convmsg)
		self.chanSym = self.addSync(imsg)
		return self.chanSym

	# encodes the call sign passed in the constructor into a 28 bit integer
	# returns 28 bit integer representing data symbols for call sign
	def encodeCallsign(self):
		# Force third charcter to be a number
		while self.callstr[2] not in string.digits:
			self.callstr = " " + self.callstr
		# pad callsign to 6 character length
		if len(self.callstr) < 6:
			self.callstr += (6-len(self.callstr))*" "
		# compress callsign into 32 bits
		charlist = []

		for c in self.callstr:
			if c in string.digits:
				charlist.append(ord(c)-ord("0"))
			elif c in string.ascii_uppercase:
				charlist.append(ord(c)-ord("A")+10)
			elif c == " ":
				charlist.append(36)
			else:
				print("Illegal character in callsign!")
				return -1

		N = charlist[0]
		N = N*36 + charlist[1]
		N = N*10 + charlist[2]
		N = N*27 + charlist[3] - 10
		N = N*27 + charlist[4] - 10
		N = N*27 + charlist[5] - 10

		return N

	# encodes the locator string and power level passed in the constructor
	# into a 22 bit integer
	# returns 22 bit integer containing data symbols for locator and power
	def encodeLocator(self):
		charlist = []
		for c in self.locstr:
			if c in string.digits:
				charlist.append(ord(c)-ord("0"))
			elif c in string.ascii_uppercase[:18]:
				charlist.append(ord(c)-ord("A"))
			else:
				print("Illegal character in Locator")
				return -1

		M = (179 - 10*charlist[0] - charlist[2]) * 180 + 10*charlist[1] + charlist[3]
		M = M*128 + self.pwr + 64
		return M

	# stuffs M and N together into 88 bit message and applies WSPR convolutional
	# code
	# returns a list of integers in range [0,1]
	def convoCode(self,M,N):
		reg0 = 32*"0"
		reg1 = 32*"0"
		outstr = ""
		# stuff 88 bits together
		bitstr = "{0:028b}{1:022b}".format(M,N) + 31*"0"

		# apply convolutional code
		for b in bitstr:
			# shift bit into LSB
			reg0 = reg0[1:] + b
			# apply taps and truncate to 32 bits
			tmp = "{0:032b}".format(int(reg0,2) & 0xF2D05351)
			# calculate odd parity
			if tmp.count("1")%2:
				outstr += "1"
			else:
				outstr += "0"

			# shift bit into LSB
			reg1 = reg1[1:] + b
			# apply taps and truncate to 32 bits
			tmp = "{0:032b}".format(int(reg1,2) & 0xE4613C47)
			# calculate odd parity
			if tmp.count("1")%2:
				outstr += "1"
			else:
				outstr += "0"

		return list(outstr)

	# takes the raw data symbols in convstr and interleaves them according to the
	# WSPR protocol standard
	# returns a list of integers in range [0,1] which represent interleaved data symbols
	def interleave(self,convstr):
		dest = list(162*[0])
		p = 0

		for i in range(0,256):
			# j contains the bit reversal of i
			j = int("{0:08b}".format(i)[::-1],2)
			# swap the bits if needed
			if j < 162:
				dest[j] = int(convstr[p],2)
				p += 1
			# maximum of 162 data symbols need to be interleaved
			if p >= 162:
				break

		return dest

	# combines the interleaved data symbols in istr with the pseudorandom
	# WSPR synchronization vector to generate the 4-FSK channel symbols
	def addSync(self,istr):
		cs = []
		for i in range(0,162):
			s = self.syncVector[i] + 2*istr[i]
			cs.append(s)
		return cs
