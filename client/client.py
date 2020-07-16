import socket
s = socket.socket()
host = input(str("Please enter the host address of the sender: "))
port = 5000
s.connect((host,port))
print("Connected")

#filename = input(str("Enter a filename: "))
file = open("receivedFile.txt", 'wb')
file_data = s.recv(1024)
file.write(file_data)
file.close()
print("File has been receieved")