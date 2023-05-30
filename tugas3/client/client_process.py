import socket
import logging
from multiprocessing import Process

logging.basicConfig(level=logging.INFO)


def kirim_data(nama="kosong"):
    # membuat koneksi dengan server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 45000)
    sock.connect(server_address)
    # logging.info(f"client {nama} connect to socket {server_address}")

    try:
        # Send data
        message = 'TIME\r\n\r\n'
        logging.warning(f"[CLIENT {nama+1}] sending {message.encode()}")
        sock.sendall(message.encode())

        # menerima data
        data_received = ''
        while True:
            data = sock.recv(16)
            data_received += data.decode()
            if "\r\n\r\n" in data_received:
                break
            else:
                # Data kosong
                break
            
            # menghapus \r\n\r\n
        data_received = data_received.strip()
        # logging.info(f"JAM {data_received}")
    finally:
        # logging.warning("closing")
        sock.close()
    return


if __name__=='__main__':
    process = []
    total = 5000
    for i in range(total):
        t = Process(target=kirim_data, args=(i,))
        process.append(t)

    for p in process:
        p.start()