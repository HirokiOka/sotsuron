import socket

host = "10.32.130.25"
port = 10001

client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1.connect((host, port))
client1.send("nekodayo".encode('utf-8'))
