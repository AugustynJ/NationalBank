import sqlite3
import hashlib

with open('salt', 'r') as salt_file:
    salt = salt_file.read()

db_conn = sqlite3.connect("database.db")

cursor = db_conn.cursor()

# print((cursor.execute("SELECT password FROM credentials WHERE login='login'")).fetchall())

cursor.execute('''
CREATE TABLE IF NOT EXISTS credentials (
    login varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    PRIMARY KEY(login)
)
''')
login = "user"
password = "pass"
password = password + salt
password = hashlib.sha256(password.encode()).hexdigest()
print(password)

cursor.execute("INSERT INTO credentials VALUES (?, ?)", (login, password))
db_conn.commit()

print((cursor.execute("SELECT * FROM credentials")).fetchall())

db_conn.close()
