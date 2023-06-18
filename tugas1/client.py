import sys
import socket
import logging

#set basic logging
logging.basicConfig(level=logging.INFO)



try:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.16.16.101', 32444)
    logging.info(f"connecting to {server_address}")
    sock.connect(server_address)

    message = 'INI ADALAH DATA YANG DIKIRIM ABCDEFGHIJKLMNOPQ'
    print('message =', type(message))
    logging.info(f"sending {message}")
    sock.sendall(message.encode())

    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        print("client check 2")
        data = sock.recv(16)
        print("client check 3")
        amount_received += len(data)
        print("client check 4")
        logging.info(f"{data}")

except Exception as ee:
    logging.info(f"ERROR: {str(ee)}")
    exit(0)
finally:
    logging.info("closing")
    sock.close()
