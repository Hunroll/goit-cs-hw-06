import socket
from concurrent import futures as cf
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from datetime import datetime

def connect(mongo_url):
    mongo_url = mongo_url + '?retryWrites=true&w=majority&appName=hw6'
    try:
        client = MongoClient(mongo_url, server_api=ServerApi('1'))
        return client.book
    except Exception as e:
        print("Error connecting to DB!")
        print(e)
        return None
    
def run_server(ip, port, mongodb_url):
    def handle(sock: socket.socket, address: str):
        print(f'Connection established {address}')
        while True:
            try:
                received = sock.recv(1024)
                if not received:
                    break
                data = received.decode()
                print(f'Data received: {data}')
                message = json.loads(data)
                message["date"] = datetime.now()
                print("Saving:", message)
                db.messages.insert_one(message)
            except Exception as err:
                print("Failed to process the message", data, "\nError:", err)
        print(f'Socket connection closed {address}')
        sock.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(10)

    db = connect(mongodb_url)
    print(f'Start socket server {server_socket.getsockname()}')
    with cf.ThreadPoolExecutor(20) as client_pool:
        try:
            while True:
                new_sock, address = server_socket.accept()
                client_pool.submit(handle, new_sock, address)
        except KeyboardInterrupt:
            print(f'Destroy server')
        except Exception as err:
            print("Other error:", err)
        finally:
            server_socket.close()