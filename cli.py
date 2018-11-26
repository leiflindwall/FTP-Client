
# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys
import re

def put_file(file_name):


	# Create a socket for the data channel
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to port 0
	dataSock.bind(('',0))

	# Retreive the ephemeral port number
	print "I chose ephemeral port as the data channel: ", dataSock.getsockname()[1]



	# Open the file
	fileObj = open(file_name, "r")
	# The number of bytes sent
	numSent = 0

	# The file data
	fileData = None

	# Keep sending until all is sent
	while True:
		
		# Read 65536 bytes of data
		fileData = fileObj.read(65536)
		
		# Make sure we did not hit EOF
		if fileData:
			
				
			# Get the size of the data read
			# and convert it to string
			dataSizeStr = str(len(fileData))
			
			# Prepend 0's to the size string
			# until the size is 10 bytes
			while len(dataSizeStr) < 10:
				dataSizeStr = "0" + dataSizeStr
		
		
			# Prepend the size of the data to the
			# file data.
			fileData = dataSizeStr + fileData	
			
			# The number of bytes sent
			numSent = 0
			
			# Send the data!
			while len(fileData) > numSent:
				numSent += dataSock.send(fileData[numSent:])
		
		# The file has been read. We are done
		else:
			break


	print "Sent ", numSent, " bytes."
		
	
	fileObj.close()

def get_file(file_name):
	
	# Create a socket for the data channel
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to port 0
	dataSock.bind(('',0))

	#dataSock.listen(1)

	# Retreive the ephemeral port number
	print "I chose ephemeral port as the data channel: ", dataSock.getsockname()[1]

	# The number of bytes sent
	numSent = 0

	# send the ephemeral port # to the server first
	# Keep sending until all is sent
	while True:
		
		# write the data socket port & filename to the data
		fileData = str(dataSock.getsockname()[1]) + " " + "get " + file_name

		# try padding data
		# Prepend 0's to the size string
			# until the size is 10 bytes
		#while len(fileData) < 30:
			#fileData = "0" + fileData
		
		# Make sure we did not hit EOF
		if fileData:
			
				
			# Get the size of the data read
			# and convert it to string
			dataSizeStr = str(len(fileData))
			
			# Prepend 0's to the size string
			# until the size is 10 bytes
			while len(dataSizeStr) < 10:
				dataSizeStr = "0" + dataSizeStr
		
		
			# Prepend the size of the data to the
			# file data.
			fileData = dataSizeStr + fileData	
			
			# The number of bytes sent
			numSent = 0
			
			# Send the data!
			while len(fileData) > numSent:
				numSent += connSock.send(fileData[numSent:])
		
		# The file has been read. We are done
		else:
			break

	dataSock.listen(1)

	print "Sent ", numSent, " bytes."

	# download the file
	# Accept connections forever
	while True:
		
		print "Waiting for connections..."
			
		# Accept connections
		clientSock, addr = dataSock.accept()
		
		print "Accepted connection from server: ", addr
		print "\n"
		
		# The buffer to all data received from the
		# the client.
		fileData = ""
		
		# The temporary buffer to store the received
		# data.
		recvBuff = ""
		
		# The size of the incoming file
		fileSize = 0	
		
		# The buffer containing the file size
		fileSizeBuff = ""
		
		# Receive the first 10 bytes indicating the
		# size of the file
		fileSizeBuff = recvAll(clientSock, 10)
			
		# Get the file size
		fileSize = int(fileSizeBuff)
		
		print "The file size is ", fileSize
		
		# Get the file data
		fileData = recvAll(clientSock, fileSize)
		
		print "The file data is: "
		print fileData

		# Close the  data socket and the file
		dataSock.close()
		
# for GET command
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


	
# "main" program
# Command line checks 
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <Port #>" 

# Server address
serverAddr = "localhost"

# Server port
serverPort = int(sys.argv[1])

# The name of the file
#fileName = sys.argv[1]

# Open the file
#fileObj = open("file.txt", "r")

# Create a TCP socket for control channel
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))





done = False

while done == False:
	#print "ftp> "
	current_cmd = raw_input("ftp> ")
	if "get" in current_cmd:
		print("in get cmd")
		get_file("file.txt")
	elif "put" in current_cmd:
		print("in put cmd")
		put_file("file.txt")
	elif "ls" in current_cmd:
		print("in ls cmd")
	else:
		done = True
		#quit

# Close the socket and the file
connSock.close()
		




