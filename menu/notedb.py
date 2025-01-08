import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the notes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    iduser INTEGER NOT NULL,
    idmodule INTEGER NOT NULL,
    note REAL NOT NULL,
    FOREIGN KEY (iduser) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (idmodule) REFERENCES modules (id) ON DELETE CASCADE
)
''')

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Notes table created successfully.")
