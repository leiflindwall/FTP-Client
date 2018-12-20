# FTP-Client
CPSC471 Socket Programming Assignment: FTP Client

Michael Lindwall michaellindwall@csu.fullerton.edu

Marcus Hoertz marcus.hoertz@csu.fullerton.edu

These scripts were written in Python 2.7.  

To run this application:

-navigate to the directory where these scripts & any files to transfer, 
and begin by starting the server with the command 'python serv.py <port #>'.  

-start the client with the command 'python cli.py <server IP/hostname> <server port #>'.

-You should see a prompt 'ftp> '.  Supply one of the following commands:

  get <file name>     *this downloads the specified file from the server
  
  put <file name>     *this uploads the specified file to the server
  
  ls                  *this list the files on the server (only works on linux)
  
  quit                *this quits the ftp client

  -Special Notes:
  This project was written mostly on windows using Visual Studio Code and the Windows Python 2.7 Interpretter.  When running on localhost on windows, we had no trouble 
  with the socket refusing connections.  When we switched to Linux to test the LS command, we unpredictably get the connection closed, sometimes after 8 successful commands, sometimes after 2.  We did not have time to investigate why this happens so unpredictably, and only when running on a linux machine.



