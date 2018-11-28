
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket

# the method to connect to the client's data socket
def connect_data_socket(file_data):
	data_port = int(file_data.rsplit(" ", 2)[0])
	file_name = str(file_data.rsplit(" ", 2)[2])
	
	print "connecting to data socket..."
	print "data port #: " + str(data_port)
	print "file name: " + str(file_name)

	cliAddr = "localhost"
	#cliPort = 1234

	# Create a TCP socket
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the client's data port
	dataSock.connect((cliAddr, data_port))

	return dataSock


def create_data_sock(command):
	# Create a socket for the data channel
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to port 0
	#dataSock.bind(('',0))
	dataSock.bind(('',1235))

	# start listening on that port
	dataSock.listen(1)

	# Retreive the ephemeral port number
	#print "I chose ephemeral port as the data channel: ", dataSock.getsockname()[1]
	#print "sending port # to client.......\n"

	
	#print "Sent data port # to server, ", numSent, " bytes."

	return dataSock


# the method to handle the PUT command
def recv_file(file_data):
	# connect to the client's data socket
	dataSock = create_data_sock("put")

	# Accept connections forever
	
		
	print "Waiting for connections for file transfer"
			
		# Accept connections
	clientSock, addr = dataSock.accept()
		
	print "Accepted connection from client on control channel: \n", addr
		
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
		
	print "The file data is: "
	print fileData
			
		# Close our side
	dataSock.close()


# method to handle GET command
def send_file(file_data):
	# connect to the client's data socket
	dataSock = connect_data_socket(file_data)

	#dataSock.listen(2)
	print "request from client to download file..."
		
	# Accept connections
	clientSock, addr = dataSock.accept()

	
	print "Accepted connection from client on data port: ", addr
	print "\n"

	# Open the file
	file_name = str(file_data.rsplit(" ", 2)[2])
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

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	print " reached recvALL..."
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





# THE MAIN SERVER PROGRAM

# The port on which to listen
listenPort = 1234

# Create the control socket. 
controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
controlSock.bind(('', listenPort))

# Start listening on the socket
controlSock.listen(1)
		
# Accept connections forever
print "Waiting for connections..."
		
	# Accept connections
clientSock, addr = controlSock.accept()
	
print "Accepted connection from client on control channel: \n", addr

while True:
	

	
	# The buffer to all data received from the the client.
	fileData = ""
	
	# The temporary buffer to store the received data
	recvBuff = ""
	
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
	
	#print "The file data is: "
	#print fileData

	if "get" in fileData:
		print("received get cmd ... attempting to send file")
		send_file(fileData)
	elif "put" in fileData:
		print("received put cmd ... attempting to receive file")
		recv_file(fileData)
		
# Close our side
clientSock.close()
	
