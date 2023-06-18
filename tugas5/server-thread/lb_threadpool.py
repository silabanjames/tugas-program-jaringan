from socket import *
import socket
import time
import sys
import logging
from concurrent.futures import ThreadPoolExecutor
from http import HttpServer

class BackendList:
    def __init__(self):
        self.servers=[]
        self.servers.append(('127.0.0.1',9032))
        self.servers.append(('127.0.0.1',9033))
        self.servers.append(('127.0.0.1',9034))
        self.servers.append(('127.0.0.1',9035))
        self.current=0
    def getserver(self):
        s = self.servers[self.current]
        print(s)
        self.current=self.current+1
        if (self.current>=len(self.servers)):
            self.current=0
        return s

def Backend(backend_connection, client_connection, backend_address, client_address):
    try:
        rcv=''
        while True:
            # print(f'BACKEND untuk {client_address} menunggu...')
            data = client_connection.recv(1024)
            rcv += data.decode()
            if rcv[-2:] == '\r\n':
                backend_connection.sendall(rcv.encode())
                # print(f'dari {client_address} akan dikirim {rcv} ke BACKEND')
                break
            else:
                break
    except Exception as e:
        logging.warning(f"error backend: {e}")
    # finally:
        # backend_connection.close()
        
    
def ProcessTheClient(backend_connection, client_connection, backend_address, client_address):
    try:
        rcv=''
        while True:
            # print(f'PTC kepada {client_address} menunggu ...')
            data = backend_connection.recv(1024)
            rcv += data.decode()
            if '\r\n\r\n' in rcv:
                client_connection.sendall(rcv.encode())
                # print(f'Pesan PTC masuk dan akan dikirim {rcv} ke {client_address}')
                break
                # client_connection.close()
            else:
                break
    except Exception as e:
        logging.warning(f"error client: {e}")
    finally:
        backend_connection.close()
        client_connection.close()

def Server():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    backend = BackendList()

    my_socket.bind(('0.0.0.0', 1111))
    my_socket.listen(5)
    logging.warning("load balancer running on port {}".format(1111))

    with ThreadPoolExecutor() as executor:
        while True:
                client_connection, client_address = my_socket.accept()
                # print(f"Received connection from {client_address}")
                backend_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # backend_connection.settimeout(1)
                backend_address = backend.getserver()
                logging.warning(f"koneksi dari {client_address} diteruskan ke {backend_address}")
                try:
                    backend_connection.connect(backend_address)
                    # print(f"Connected to backend {backend_address}")
                    #logging.warning("connection from {}".format(client_address))
                    toserver = executor.submit(Backend, backend_connection, client_connection, backend_address, client_address)
                    #the_clients.append(toupstream)
                    toclient = executor.submit(ProcessTheClient, backend_connection, client_connection, backend_address, client_address)
                    #the_clients.append(toclient)
                    
                    # toupstream = executor.submit(ProcessTheClient, client_connection, client_address,backend_connection,'toupstream')
                    # #the_clients.append(toupstream)
                    # toclient = executor.submit(ProcessTheClient, client_connection, client_address,backend_connection,'toclient')

                except Exception as err:
                    logging.error(err)
                    pass

def main():
	Server()

if __name__=="__main__":
	main()