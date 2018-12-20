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
import commands
import ftp

# this method sends the command to the server on the control channel
def send_command(command):
	# The number of bytes sent
	numSent = 0

	# The file data
	fileData = None

	# write the command & filename to the data
	if(command == "ls"):
		fileData=command
	else:
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

# the method to handle the PUT command
def put_file(file_name):
	# send the put command to the server
	send_command("put")

	# connect to data socket 1235
	dataSock = ftp.connect_data_socket()

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
		print "PUT SUCCESSFUL\n"
		
	# Close the socket and the file
	dataSock.close()
	fileObj.close()

# the method to handle the GET command
def get_file(file_name):
	# send the put command to the server
	send_command("get")

	# create the data socket for file transfer
	dataSock = ftp.create_data_sock()

	print "Waiting for connections for file transfer......"
			
	# Accept connections
	clientSock, addr = dataSock.accept()	
	print "Accepted connection from client on data channel: ", addr
		
	# The size of the incoming file
	fileSize = 0	
		
	# The buffer containing the file size
	fileSizeBuff = ""
		
	# Receive the first 10 bytes indicating the size of the file
	fileSizeBuff = ftp.recvAll(clientSock, 10)
			
	# Get the file size
	fileSize = int(fileSizeBuff)

	# Get the file data containing the command from the connection socket
	fileData = ftp.recvAll(clientSock, fileSize)
		
	if fileData:
		print "\nGET SUCCESSFUL"
		print "\nThe file data is: "
		print fileData
	else:
		print "GET FAILED"
			
	# Close our side
	dataSock.close()

def ls_response():
	print "Waiting for ls response......"
			
	# Accept connections
	servSock, addr = dataSock.accept()	
	#print "Accepted connection from client on control channel: ", addr
		
	# The size of the incoming file
	fileSize = 0	
		
	# The buffer containing the file size
	fileSizeBuff = ""
		
	# Receive the first 10 bytes indicating the size of the file
	fileSizeBuff = ftp.recvAll(servSock, 10)
			
	# Get the file size
	fileSize = int(fileSizeBuff)

	# Get the file data containing the command from the connection socket
	fileData = ftp.recvAll(servSock, fileSize)
		
	if fileData:
		print "\nLS SUCCESSFUL"
		print "\nThe response data is: "
		print fileData
	else:
		print "GET FAILED"

	dataSock.close()
			
	
# THE MAIN CLIENT PROGRAM

# Command line checks 
if len(sys.argv) < 3:
	print "USAGE: python " + sys.argv[0] + " <SERVER IP/HOSTNAME> <SERVER PORT>" 

# Server address
#serverAddr = "localhost"
serverAddr = sys.argv[1]

# Server port
#serverPort = 1234
serverPort = int(sys.argv[2])

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
		send_command("ls")
		dataSock = ftp.create_data_sock()
		ls_response()
		#dataSock.close()
	else:
		print("Terminating control connection")
		done = True

# Close the socket
controlSock.close()