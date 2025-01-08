import sqlite3
from faker import Faker
import random

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    image BLOB,
    level TEXT NOT NULL
)
''')

# Initialize Faker for generating fake data
faker = Faker()

# Function to generate fake user data
def generate_fake_user():
    username = faker.user_name()
    email = faker.email()
    password = faker.password()
    image = faker.image()  # Placeholder for a binary image, set to None
    level = random.choice(['S1', 'S2', 'S3', 'S4'])  # Randomly assign a level
    return username, email, password, image, level

# Insert fake data into the users table
num_records = 40  # Number of fake users to generate
for _ in range(num_records):
    user_data = generate_fake_user()
    cursor.execute('''
    INSERT INTO users (username, email, password, image, level)
    VALUES (?, ?, ?, ?, ?)
    ''', user_data)

# Commit the transaction and close the connection
conn.commit()
conn.close()

print(f'{num_records} fake users have been inserted into the users table with levels.')
