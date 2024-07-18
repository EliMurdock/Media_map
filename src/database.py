import sqlite3
import hashlib
import json



def create_sql_db():
    conn = sqlite3.connect("data/userdata.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        last_search TEXT NOT NULL)
    """)

    conn.commit()
    conn.close()


def add_user(username, password):
    conn = sqlite3.connect("data/userdata.db")
    cur = conn.cursor()

    password = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("INSERT INTO userdata (username, password, last_search) VALUES (?, ?, ?)", (username, password, ""))
    conn.commit()


#update movie data for a user
def update_last_search(username, last_search):
    conn = sqlite3.connect("data/userdata.db")
    cur = conn.cursor()
    

    # converter for bad  data types



    json_data = json.dumps(last_search, default=str)
    cur.execute("UPDATE userdata SET last_search = ? WHERE username = ?", (json_data, username))
    conn.commit()

    conn.close()


#gets data from the last search done
def get_last_search(username):
    conn = sqlite3.connect("data/userdata.db")
    cur = conn.cursor()

    cur.execute("SELECT last_search FROM userdata WHERE username = ?", (username,))

    json_result = cur.fetchone()
    conn.close()
    if json_result[0]:
        last_search = json.loads(json_result[0])
        return last_search
    else:
        return None


if __name__ == "__main__":
    create_sql_db()