import sqlite3
import hashlib



def create_sql_db():
    conn = sqlite3.connect("data/userdata.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL),
        last_search TEXT NOT NULL)
    """)

    username1, password1 = "deliveryman", hashlib.sha256("package1!".encode()).hexdigest()
    username2, password2 = "critic", hashlib.sha256("movie".encode()).hexdigest()

    cur.execute("INSERT INTO userdata (username, password, last_search) VALUES (?, ?, ?)", (username1, password1, ""))
    cur.execute("INSERT INTO userdata (username, password, last search) VALUES (?, ?, ?)", (username2, password2, ""))

    conn.commit()


#update movie data for a user
def update_last_search(username, last_search):
    conn = sqlite3.connect("data/userdata.db")
    cur = conn.cursor()

    cur.execute("UPDATE userdata SET last_search = ? WHERE username = ?", (last_search, username))
    conn.commit()

    conn.close()


#gets data from the last search done
def get_last_search(username):
    conn = sqlite3.connect("data/userdata.db")
    cur = conn.cursor()

    cur.execute("SELECT last_search FROM userdata WHERE username = ?", (username,))
    result = cur.fetchone()
    result = result[0]
    conn.close()

    if result == "":
        return None
    else:
        return result


if __name__ == "__main__":
    create_sql_db()