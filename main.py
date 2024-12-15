import src.httpServer as hs
import src.socketServer as ss
import os

from concurrent import futures as cf
        
SOCKET_SERVER_HOST="localhost"
SOCKET_SERVER_PORT=5000

if __name__ == "__main__":
    MONGO_URL = os.environ['MONGO_URL']
    try:
        with cf.ProcessPoolExecutor(2) as client_pool:
            client_pool.submit(ss.run_server, SOCKET_SERVER_HOST, SOCKET_SERVER_PORT, MONGO_URL)
            client_pool.submit(hs.run, SOCKET_SERVER_HOST, SOCKET_SERVER_PORT)
    except KeyboardInterrupt:
        print("exiting")
    except Exception as err:
        print("Unhandled error:", err)
    finally:
        os.kill(os.getpid(), 9)

        