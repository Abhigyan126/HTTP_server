
import os

class HandleMethod():
    def __init__(self, data, directory, conn):
        self.data = data
        self.directory = directory
        self.conn = conn

    def GET(self, data, directory, conn):
        if data.get("method") == "GET":
            path = data.get("path")
            if "/" not in path:
                path += "/"
            if path == "/":
                response = (b"HTTP/1.1 200 OK\r\n\r\n")
            elif path.startswith("/echo/"):
                path = path.replace("/echo/", "")
                response = str.encode(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path)}\r\n\r\n{path}\r\n")
            elif path.startswith("/user-agent"):
                agent = data.get("user-agent", "Unknown")
                agent = agent.split(" ")[0]
                response = str.encode(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(agent)}\r\n\r\n{agent}\r\n")
            elif path.startswith("/files/"):
                filename = path.replace("/files/", "")
                if directory and os.path.isdir(directory):
                        filepath = os.path.join(directory, filename)
                        if os.path.isfile(filepath):
                            with open(filepath, "rb") as file_object:
                                content = file_object.read()
                            response = (
                            f"HTTP/1.1 200 OK\r\n"
                            f"Content-Type: application/octet-stream\r\n"
                            f"Content-Length: {len(content)}\r\n"
                            f"\r\n"
                            ).encode() + content
                        else:
                            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
                else:
                    response = b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
            else:
                response = (b"HTTP/1.1 404 Not Found\r\n\r\n")
            conn.send(response)

    def POST(self,data,directory,conn):
        if data.get("method") == "POST":
            path = data.get("path")
            if path.startswith("/files/"):
                if directory and os.path.isdir(directory):
                        filename = path.replace("/files/", "")
                        filepath = os.path.join(directory, filename)
                        content_length = int(data.get("Content-Length", 0))
                        with open(filepath, "w") as file_object:
                            file_object.write(data)
                        response = (
                        f"HTTP/1.1 201 Created\r\n"
                        f"Content-Type: text/plain\r\n"
                        f"Content-Length: {len('File created!')}\r\n"
                        f"\r\n"
                        f"File created!"
                        )
                        conn.send(response.encode())      
                else:
                    conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")             
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
    def PUT(self, data, directory, conn):
        if data.get("method") == "PUT":
            path = data.get("path")
            if path.startswith("/files/"):
                if directory and os.path.isdir(directory):
                        filename = path.replace("/files/", "")
                        filepath = os.path.join(directory, filename)
                        content_length = int(data.get("Content-Length", 0))
                        with open(filepath, "a") as file_object:
                            file_object.write(data)
                        response = (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: text/plain\r\n"
                        f"Content-Length: {len('File updated!')}\r\n"
                        f"\r\n"
                        f"File updated!"
                        )
                        conn.send(response.encode())       
                else:
                    conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")           
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")

    def DELETE(self, data, directory, conn):
        if data.get("method") == "DELETE":
            path = data.get("path")
            if path.startswith("/files/"):
                if directory and os.path.isdir(directory):
                    filename = path.replace("/files/", "")
                    filepath = os.path.join(directory, filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                        response = (
                            f"HTTP/1.1 200 OK\r\n"
                            f"Content-Type: text/plain\r\n"
                            f"Content-Length: {len('File deleted!')}\r\n"
                            f"\r\n"
                            f"File deleted!"
                            )
                        conn.send(response.encode())
                    else:
                        conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n") 
                else:
                    conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
            else:
                conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
            
            
            


"""
from unittest.mock import Mock

# Test code
def test_handle_method():
    # Mock data
    data = {
        "method": "GET",
        "path": "/files/test.txt",
        "User-Agent": "Mozilla/5.0",
        "Content-Length": 0  # Assuming no payload for simplicity
    }
    directory = "./test_directory"
    
    # Create a mock connection object
    conn = Mock()

    # Initialize HandleMethod instance
    handle_method = HandleMethod(data, directory, conn)

    # Test GET method
    print("Testing GET method...")
    handle_method.GET(data, directory, conn)
    print("GET method test complete.")

    # Test POST method
    print("\nTesting POST method...")
    handle_method.POST(data, directory, conn)
    print("POST method test complete.")

    # Test PUT method
    print("\nTesting PUT method...")
    handle_method.PUT(data, directory, conn)
    print("PUT method test complete.")

    # Test DELETE method
    print("\nTesting DELETE method...")
    handle_method.DELETE(data, directory, conn)
    print("DELETE method test complete.")

    # Test error handling
    print("\nTesting error handling...")
    # Simulate error scenarios
    invalid_data = {}  # Invalid data format
    invalid_directory = "./nonexistent_directory"  # Non-existent directory

    # Test handling of invalid data format
    try:
        handle_method.GET(invalid_data, directory, conn)
    except Exception as e:
        print(f"Error handling test - Invalid data format: {e}")

    # Test handling of non-existent directory
    try:
        handle_method.POST(data, invalid_directory, conn)
    except Exception as e:
        print(f"Error handling test - Non-existent directory: {e}")

    print("Error handling test complete.")

if __name__ == "__main__":
    test_handle_method()
"""