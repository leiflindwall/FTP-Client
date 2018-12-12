# *********************************************************
# CPSC 471-01, Dr. Yun Tian
# FTP Client / Socket Programming Project
#
# Michael Lindwall michaellindwall@csu.fullerton.edu
# Marcus Hoertz marcus.hoertz@csu.fullerton.edu
#
# FTP.PY
#
# This script impliments the shared methods used by the 
# client and server scripts to create a data socket, 
# connect to a data socket, and the recvall method to 
# read the packet from the socket
# *********************************************************
import socket
import os
import sys
import commands

# the method to create the socket for data transfer
def create_data_sock():
	# Create a socket for the data channel
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to port 1235
	dataSock.bind(('',1235))

	# start listening on that port
	dataSock.listen(1)

	return dataSock

# the method to connect to a data socket
def connect_data_socket():
	print "connecting to data socket..."

	cliAddr = "localhost"
	servPort = 1235

	# Create a TCP socket
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the client's data port
	dataSock.connect((cliAddr, servPort))

	return dataSock

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):
	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff