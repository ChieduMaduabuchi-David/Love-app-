import socket
import pytz
host = socket.gethostbyname(socket.gethostname())
port = 4683


client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind((host,port))

client.accept()