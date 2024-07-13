import sqlite3
import hashlib
import socket
import threading



def handle_connection(c):
    # recieving the data from the login app
    username = c.recv(1024).decode()
    password = c.recv(1024).decode()
    password = hashlib.sha256(password.encode()).hexdigest()

    # connecting to database
    conn = sqlite3.connect("data/userdata.db")
    cur = conn.cursor()

    # searching the databse for username and password
    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
    

    # if found return success, else return fail
    if cur.fetchall():
        c.send("Login successful".encode())
    else:
        c.send("Login failed".encode())

    conn.close()
    c.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen()

    print("Server started. Waiting for connections...")

    while True:
        client,addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_connection, args=(client,)).start()



if __name__ == "__main__":
    start_server()


