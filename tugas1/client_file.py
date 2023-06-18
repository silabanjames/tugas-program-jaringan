import sys
import socket
import logging

# Timer
from datetime import datetime
from threading import Timer

# Set timer
x=datetime.today()
# # # 12 siang WIB sama dengan 5 pagi di datetime.today (perbedaan waktu 7 jam)
y=x.replace(day=x.day, hour=6, minute=38, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

#set basic logging
logging.basicConfig(level=logging.INFO)


def client():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('172.16.16.101', 32444)
        logging.info(f"connecting to {server_address}")
        sock.connect(server_address)

        # Send data

        # Open the file
        file = open("./sample.txt", "r")
        message = file.read()

        #Sending the file data to the server
        sock.send(message.encode())
        logging.info(f"File have been sended")
        file.close()

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            # print("client check 2")
            data = sock.recv(16).decode()
            # print("client check 3")
            amount_received += len(data)
            # print("client check 4")
            logging.info(f"{data}")

    except Exception as ee:
        logging.info(f"ERROR: {str(ee)}")
        exit(0)
    finally:
        logging.info("closing")
        sock.close()

t = Timer(secs, client)
t.start()

