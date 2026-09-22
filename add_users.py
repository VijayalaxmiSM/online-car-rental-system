import sqlite3

conn = sqlite3.connect('car_rental.db')
cur = conn.cursor()

cur.execute("""
INSERT INTO users (name, email, password)
VALUES
('Aruna', 'aruna@gmail.com', '1234'),
('Ravi', 'ravi@gmail.com', '1234'),
('Priya', 'priya@gmail.com', '1234')
""")

conn.commit()
conn.close()

print("Users added successfully")