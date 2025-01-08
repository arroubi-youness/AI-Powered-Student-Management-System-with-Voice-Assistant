import sqlite3
import numpy as np
import random
from faker import Faker
from face_recognition import face_encodings, load_image_file

# Initialize Faker for generating fake data
faker = Faker()

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("users.db")
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

# Function to encode a face from an image
def encode_face(image_path):
    try:
        # Load the image from the given path
        image = load_image_file(image_path)
        # Get face encodings (if a face is detected)
        encodings = face_encodings(image)
        if encodings:
            return encodings[0]  # Return the first face encoding found
        else:
            print("Aucun visage détecté dans l'image.")
            return None
    except Exception as e:
        print(f"Erreur lors de l'encodage de l'image : {e}")
        return None

# Function to register a user with face encoding
def register_user(username, email, password, image_path=None, level="S1"):
    face_encoding = None
    if image_path:
        face_encoding = encode_face(image_path)
        if face_encoding is None:
            print("Aucun visage détecté dans l'image. Enregistrement annulé.")
            return

    # Convert the face encoding to binary for database storage
    face_encoding_blob = (
        sqlite3.Binary(np.array(face_encoding, dtype=np.float32).tobytes())
        if face_encoding is not None
        else None
    )

    # Insert the user data into the users table
    cursor.execute('''
    INSERT INTO users (username, email, password, image, level)
    VALUES (?, ?, ?, ?, ?)
    ''', (username, email, password, face_encoding_blob, level))

    conn.commit()
    print(f"Utilisateur '{username}' enregistré avec succès.")

# Function to generate and register fake users
def generate_fake_users(num_records=10, image_path=None):
    for _ in range(num_records):
        username = faker.user_name()
        email = faker.email()
        password = faker.password()
        level = random.choice(['S1', 'S2', 'S3', 'S4'])
        register_user(username, email, password, image_path, level)

# Specify the path to the default image
image_path = "C:/Users/pc/Desktop/ro.jpeg"  # Replace with your image path

# Generate 10 fake users with the specified image
generate_fake_users(10, image_path)

# Close the database connection
conn.close()
print("Tous les utilisateurs fictifs ont été enregistrés avec succès.")


