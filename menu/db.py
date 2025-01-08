import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the modules table
cursor.execute('''
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester TEXT NOT NULL,
    module_name TEXT NOT NULL
)
''')

# Insert data into the modules table
modules_data = [
    ('S1', 'Analyse 1'),
    ('S1', 'Algebre 1'),
    ('S1', 'Mecanique point'),
    ('S1', 'Langue'),
    ('S1', 'Thermodynamique'),
    ('S2', 'Thermochimie'),
    ('S2', 'Analyse 2'),
    ('S2', 'Algebre 2'),
    ('S2', 'Circuit electronique'),
    ('S2', 'Langue 2'),
    ('S3', 'Thermochimie 2'),
    ('S3', 'Analyse 3'),
    ('S3', 'Algebre 3'),
    ('S3', 'Circuit electronique 2'),
    ('S3', 'Langue 3'),
('S4', 'Thermochimie 2'),
    ('S4', 'Analyse 4'),
    ('S4', 'Algebre 4'),
    ('S4', 'Circuit electronique 3'),
    ('S4', 'Langue 4')

]

# Insert the data
cursor.executemany('''
INSERT INTO modules (semester, module_name) VALUES (?, ?)
''', modules_data)

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Modules table created and data inserted successfully.")
