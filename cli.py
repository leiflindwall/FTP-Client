# *********************************************************
# CPSC 471-01, Dr. Yun Tian
# FTP Client / Socket Programming Project
#
# Michael Lindwall michaellindwall@csu.fullerton.edu
# Marcus Hoertz marcus.hoertz@csu.fullerton.edu
#
# CLI.PY
#
# This script impliments the client-side of an FTP client
# *********************************************************
import socket
import os
import sys

# this method sends the command to the server on the control channel
def send_command(command):
	# The number of bytes sent
	numSent = 0

	# The file data
	fileData = None

	# write the command & filename to the data
	fileData = str(command + " " + file_name)

	# Keep sending until all is sent
	while True:

		# Make sure we did not hit EOF
		if fileData:
							
			# Get the size of the data read and convert it to string
			dataSizeStr = str(len(fileData))
			
			# Prepend 0's to the size string until the size is 10 bytes
			while len(dataSizeStr) < 10:
				dataSizeStr = "0" + dataSizeStr
				
			# Prepend the size of the data to the file data.
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

	print "\nSent command to server, ", numSent, " bytes."

	
# the method to connect to the server's data socket
def connect_data_socket():
	print "connecting to data socket..."

	cliAddr = "localhost"
	servPort = 1235

	# Create a TCP socket
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the client's data port
	dataSock.connect((cliAddr, servPort))

	return dataSock

# the method to create the socket for data transfer
def create_data_sock():
	# Create a socket for the data channel
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to port 1235
	dataSock.bind(('',1235))

	# start listening on that port
	dataSock.listen(1)

	return dataSock


# the method to handle the PUT command
def put_file(file_name):
	# send the put command to the server
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
							
			# Get the size of the data read and convert it to string
			dataSizeStr = str(len(fileData))
			
			# Prepend 0's to the size string until the size is 10 bytes
			while len(dataSizeStr) < 10:
				dataSizeStr = "0" + dataSizeStr
				
			# Prepend the size of the data to the file data.
			fileData = dataSizeStr + fileData	
			
			# The number of bytes sent
			numSent = 0
			
			# Send the data!
			while len(fileData) > numSent:
				numSent += dataSock.send(fileData[numSent:])
		
		# The file has been read. We are done
		else:
			break

	print "Sent "+ file_name + ", ", numSent, " bytes.\n"
		
	# Close the socket and the file
	dataSock.close()
	fileObj.close()


# the method to handle the GET command
def get_file(file_name):
	# send the put command to the server
	send_command("get")

	# create the data socket for file transfer
	dataSock = create_data_sock()

	print "Waiting for connections for file transfer......"
			
	# Accept connections
	clientSock, addr = dataSock.accept()	
	print "Accepted connection from client on data channel: ", addr
		
	# The size of the incoming file
	fileSize = 0	
		
	# The buffer containing the file size
	fileSizeBuff = ""
		
	# Receive the first 10 bytes indicating the size of the file
	fileSizeBuff = recvAll(clientSock, 10)
			
	# Get the file size
	fileSize = int(fileSizeBuff)

	# Get the file data containing the command from the connection socket
	fileData = recvAll(clientSock, fileSize)
		
	if fileData:
		print "\nGET SUCCESSFUL"
		print "\nThe file data is: "
		print fileData
	else:
		print "GET FAILED"
			
	# Close our side
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

# Server address
serverAddr = "localhost"

# Server port
serverPort = 1234

# Create a TCP socket for control channel
controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
controlSock.connect((serverAddr, serverPort))

done = False
while done == False:
	current_cmd = raw_input("ftp> ")

	if "get" in current_cmd:
		file_name = str(current_cmd.rsplit(" ", 2)[1])
		# Open the file
		fileObj = open(file_name, "r")
		get_file(file_name)
	elif "put" in current_cmd:
		file_name = str(current_cmd.rsplit(" ", 2)[1])
		# Open the file
		fileObj = open(file_name, "r")
		put_file(file_name)
	elif "ls" in current_cmd:
		print("in ls cmd")
	else:
		done = True

# Close the socket
controlSock.close()
		




