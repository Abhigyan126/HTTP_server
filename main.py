import socket
from concurrent.futures import ThreadPoolExecutor
import datetime
import os
import sys
from HandleMethod import HandleMethod

class Httpserver():
    def __init__(self, ip="localhost", port=4221, max_workers=10, directory=None):
        self.ip = ip
        self.port = port
        self.max_workers = max_workers
        self.directory = directory
        self.ssl_socket = None
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def start_server(self):
        try:
            print(f"Server starting on {self.ip}:{self.port} at {datetime.datetime.now()}")
            self.server_socket = socket.create_server((self.ip, self.port), reuse_port=True)
            self.server_socket.settimeout(None)
            while True:
                conn, address = self.server_socket.accept()
                self.executor.submit(self.handle_client, conn, address, self.directory)
        except KeyboardInterrupt:
            print("Server shutting down...")
            self.server_socket.close()
            self.executor.shutdown(wait=False)
            print("All connections closed.")
        except Exception as error:
            print(f"Error: {error}")
    
    def handle_client(self, conn, address, directory):
        try:
            print(f"Connection from {address}")
            while True:
                request_data = b''
                while True:
                    chunk = conn.recv(1024)
                    if not chunk:
                        break
                    request_data += chunk
                    if b'\r\n\r\n' in request_data:
                        break
                if not request_data:
                    break
                request_data = request_data.decode("utf-8")
                request_data = self.parse_request(request_data)
                handle_method = HandleMethod(request_data, directory, conn)
                method_functions = {
                    "GET": handle_method.GET,
                    "POST": handle_method.POST,
                    "PUT": handle_method.PUT,
                    "DELETE": handle_method.DELETE
                }
                method = request_data.get("method")
                if method in method_functions:
                    method_functions[method](request_data, directory, conn)
                else:
                    print("Unsupported HTTP method.")
                if request_data.get("connection", "").lower() != "keep-alive":
                    break
        except Exception as e:
            print(f"Error handling client request: {e}")
        finally:
            conn.close()

    def parse_request(self, string):
        try:
            data = {}
            lines = string.split("\r\n")
            data["method"], data["path"], _ = lines[0].split(" ")
            data["payload"] = lines[-1]
            for line in lines[1:]:
                if ":" in line:
                    if line.strip():
                        key, value = line.split(": ", 1)
                        data[key.lower()] = value
            return data
        except ValueError as e:
            raise ValueError("Error parsing request line: " + str(e))
        except Exception as e:
            raise ValueError("Error parsing request: " + str(e))
        
if __name__ == "__main__":
    server = Httpserver()
    server.start_server()