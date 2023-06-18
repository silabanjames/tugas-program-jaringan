from socket import *
import socket
import time
import sys
import logging
from concurrent.futures import ThreadPoolExecutor
from http import HttpServer

httpserver = HttpServer()
rcv=""

def ProcessTheClient(connection,address):
		global rcv
		try:
			data = connection.recv(1024)
			if data:
				d = data.decode()
				rcv = rcv + d
				if rcv[-2:] == '\r\n':
					# end of command, proses string
					#logging.warning("data dari client: {}".format(rcv))
					hasil = httpserver.proses(rcv)
					#hasil sudah dalam bentuk bytes
					hasil = hasil + "\r\n\r\n".encode()
					#agar bisa dioperasikan dengan string \r\n\r\n maka harus diencode dulu => bytes

					#nyalakan ketika proses debugging saja, jika sudah berjalan, matikan
					#logging.warning("balas ke  client: {}".format(hasil))
					connection.sendall(hasil) #hasil sudah dalam bentuk bytes, kirimkan balik ke client
					# print('mengirim hasil')
					rcv = ""
					connection.close()
		except:
			pass
		connection.close()
		return

def Server(portnumber=8890):
	clients = []
	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	my_socket.bind(('0.0.0.0', portnumber))
	my_socket.listen(1)
	logging.warning("running on port {}" . format(portnumber))

	with ThreadPoolExecutor() as executor:
		while True:
				client_connection, client_address = my_socket.accept()
				logging.warning("connection from {}".format(client_address))
				client = executor.submit(ProcessTheClient, client_connection, client_address)
				clients.append(client)
				#menampilkan jumlah process yang sedang aktif
				# jumlah = ['x' for i in the_clients if i.running()==True]
				# print(jumlah)

def main():
	portnumber=8890
	try:
		portnumber=int(sys.argv[1])
	except:
		pass
	svr = Server(portnumber)

if __name__=="__main__":
	main()