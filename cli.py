
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

def send_command(command):
	# The number of bytes sent
	numSent = 0

	# The file data
	fileData = None

	# write the data socket port & filename to the data
	fileData = str(command + " " + file_name)

	# send the ephemeral port # to the server first
	# Keep sending until all is sent
	while True:
		

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
				numSent += controlSock.send(fileData[numSent:])
		
			break
		# The file has been read. We are done
		else:
			break

	#dataSock.listen(1)
	print "Sent command to server, ", numSent, " bytes."
	print "waiting for data socket port #....."

	# wait for response
	#controlSock.listen(1)

	#print "Waiting for connections..."
		
	# Accept connections
	#clientSock, addr = controlSock.accept()
	
	#print "Accepted connection from server on control channel: \n", addr
	
# the method to connect to the client's data socket
def connect_data_socket():
	
	print "connecting to data socket..."


	cliAddr = "localhost"
	servPort = 1235

	# Create a TCP socket
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the client's data port
	dataSock.connect((cliAddr, servPort))

	return dataSock


# the method to generate and send the ephemeral port # to the server for the data 
def create_data_sock(command, file_name):
	# Create a socket for the data channel
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to port 0
	dataSock.bind(('',0))

	# start listening on that port
	dataSock.listen(1)

	# Retreive the ephemeral port number
	print "I chose ephemeral port as the data channel: ", dataSock.getsockname()[1]
	print "sending command to server.......\n"

	# The number of bytes sent
	numSent = 0

	# The file data
	fileData = None

	# send the ephemeral port # to the server first
	# Keep sending until all is sent
	while True:
		# write the data socket port & filename to the data
		fileData = str(dataSock.getsockname()[1]) + " " + command + " " + file_name

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
				numSent += controlSock.send(fileData[numSent:])
		
			break
		# The file has been read. We are done
		else:
			break

	#dataSock.listen(1)
	print "Sent data port # to server, ", numSent, " bytes."

	return dataSock


# the PUT command
def put_file(file_name):
	# create the socket for data transfer
	#dataSock = create_data_sock("put", file_name)
	send_command("put")

	# connect to data socket 1235
	dataSock = connect_data_socket()


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


	print "Sent "+ file_name + ", ", numSent, " bytes."
		
	# Close the socket and the file
	dataSock.close()
	fileObj.close()


# the GET command
def get_file(file_name):
	
	# create the socket for data transfer
	dataSock = create_data_sock("get", file_name)

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
		#recvBuff = ""
		
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

		# Close the data socket
		dataSock.close()


# for GET command
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





	
# THE MAIN CLIENT PROGRAM

# Command line checks 
#if len(sys.argv) < 2:
#	print "USAGE python " + sys.argv[0] + " <Port #>" 

# Server address
serverAddr = "localhost"

# Server port
#serverPort = int(sys.argv[1])
serverPort = 1234

# Create a TCP socket for control channel
controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
controlSock.connect((serverAddr, serverPort))

done = False
while done == False:
	#print "ftp> "
	current_cmd = raw_input("ftp> ")
	file_name = str(current_cmd.rsplit(" ", 2)[1])
	# Open the file
	fileObj = open(file_name, "r")

	if "get" in current_cmd:
		print("in get cmd")
		get_file(file_name)
	elif "put" in current_cmd:
		print("in put cmd")
		put_file(file_name)
	elif "ls" in current_cmd:
		print("in ls cmd")
	else:
		done = True
		#quit

# Close the socket and the file
controlSock.close()
		




