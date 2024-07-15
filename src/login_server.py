import sqlite3
import hashlib
import socket
import threading
import time


class Login_Server:
    def __init__(self):
        self.server_running = True
        self.server_socket = None
        self.login_server_thread = self.start_server_thread()

    
    def handle_connection(self, c):
        # recieving the data from the login app
        username = c.recv(1024).decode()
        password = c.recv(1024).decode()
        password = hashlib.sha256(password.encode()).hexdigest()

        # connecting to database
        conn = sqlite3.connect("data/userdata.db")
        cur = conn.cursor()

        # searching the databse for username and password
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
        result = cur.fetchone()

        # if found return success, else return fail
        if result:
            c.send("Login successful".encode())
        else:
            c.send("Login failed".encode())

        conn.close()
        c.close()

    # starts server, don't call this
    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", 9999))
        self.server_socket.listen()
        self.server_socket.settimeout(1.0)

        print("Server started. Waiting for connections...")

        while self.server_running:
            try:
                client, addr = self.server_socket.accept()
                print(f"Connection from {addr}")
                threading.Thread(target=self.handle_connection, args=(client,)).start()
            except socket.timeout:
                continue

        self.server_socket.close()

    # call this one
    def start_server_thread(self):
        login_server = threading.Thread(target=self.start_server)
        login_server.start()
        return login_server

    def stop_server(self):
        self.server_running = False
        self.login_server_thread.join()
        print('Server stopped.')


if __name__ == "__main__":
    login_server = Login_Server()
    time.sleep(10)
    login_server.stop_server()


