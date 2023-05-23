from socket import *
import socket
import threading
import logging
import datetime

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		data_received = ''
		while True:
			data = self.connection.recv(32)
			data_received += data.decode()
			if "\r\n\r\n" in data_received:
				break
			else: 
				#Jika data kosong
				break
		if data_received.strip() == "TIME":
			dataTime = datetime.datetime.now().strftime('%X')
			dataTime += "\r\n\r\n"
			self.connection.sendall(dataTime.encode())

		self.connection.close()

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		# SOCK_STREAM digunakan untuk menentukan transport dengan TCP
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0',45000))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()