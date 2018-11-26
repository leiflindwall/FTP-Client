
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket

# method to handle GET command
def send_file(file_data):
	data_port = int(file_data.rsplit(" ", 2)[0])
	file_name = str(file_data.rsplit(" ", 2)[2])
	#data_port = int(file_data[0])
	print "data port #: " + str(data_port)
	print "file name: " + str(file_name)

	# connect to the data socket
	# Server address
	serverAddr = "localhost"

	# The name of the file
	#fileName = sys.argv[1]

	# Open the file
	#fileObj = open("file.txt", "r")

	# Create a TCP socket for control channel
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the server
	dataSock.connect((serverAddr, data_port))
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






# The port on which to listen
listenPort = 1234

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(1)

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
		
# Accept connections forever
while True:
	
	print "Waiting for connections..."
		
	# Accept connections
	clientSock, addr = welcomeSock.accept()
	
	print "Accepted connection from client: ", addr
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

	if "get" in fileData:
		send_file(fileData)
		
	# Close our side
	#clientSock.close()
	
