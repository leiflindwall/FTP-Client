# *********************************************************
# CPSC 471-01, Dr. Yun Tian
# FTP Client / Socket Programming Project
#
# Michael Lindwall michaellindwall@csu.fullerton.edu
# Marcus Hoertz marcus.hoertz@csu.fullerton.edu
#
# SERV.PY
#
# This script impliments the server-side of an FTP client
# *********************************************************
import socket
import os
import sys
import commands
import ftp

# the method to show the files
def show_files():
	dataSock = ftp.connect_data_socket()
	
	fileData = ""
	for line in commands.getstatusoutput('ls -l'):
		fileData = fileData + "\n" +str(line)
		print str(line)

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
				numSent += dataSock.send(fileData[numSent:])
		
			break
		# The file has been read. We are done
		else:
			break

	print "\nSent ls results to client. Contained ", numSent, " bytes."
	dataSock.close()

# the method to handle the PUT command
def recv_file(file_data):
	# create the data socket for file transfer
	dataSock = ftp.create_data_sock()

	print "Waiting for connections on data socket for file transfer......"
			
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
		print "\nPUT SUCCESSFUL"
		print "\nThe file data is: "
		print fileData
	else:
		print "PUT FAILED"

	# Close our side
	dataSock.close()

# method to handle GET command
def send_file(file_name):	
	# connect to the client's data socket
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

	print "\nGET SUCCESSFUL"
	print "Sent "+ file_name + ", ", numSent, " bytes.\n"
		
	# Close the socket and the file
	dataSock.close()
	fileObj.close()


# THE MAIN SERVER PROGRAM

# Command line checks 
if len(sys.argv) < 2:
	print "USAGE: python " + sys.argv[0] + " <PORT #>" 

# The port on which to listen
#listenPort = 1234
listenPort = int(sys.argv[1])

# Create the control socket. 
controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
controlSock.bind(('', listenPort))

# Start listening on the socket
controlSock.listen(1)
		
# Accept connections forever
print "\nWaiting for connections..."
		
# Accept connections
clientSock, addr = controlSock.accept()
	
print "Accepted connection from client on control channel: ", addr
print

while True:
	print "Waiting for commands on the control channel..."
	
	# The buffer to all data received from the the client.
	fileData = ""
	
	# The temporary buffer to store the received data
	recvBuff = ""
	
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

	if "get" in fileData:
		print("received GET cmd ... connecting to data socket to send file\n")
		file_name = str(fileData.rsplit(" ", 2)[1])
		send_file(file_name)
	elif "put" in fileData:
		print("received PUT cmd ... creating the data socket to receive file\n")
		recv_file(fileData)
	elif "ls" in fileData:
		print("received LS CMD ... showing files")
		show_files()
		
# Close our side
clientSock.close()