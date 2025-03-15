import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('./todo.db')
cursor = conn.cursor()

# Create the 'todo' table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, 
        description TEXT,
        priority INTEGER,
        complete  BOOLEAN
    );
""")

# List all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:", tables)

# For example, if you have a table named 'todo', query it:
cursor.execute("SELECT * FROM todo;")
rows = cursor.fetchall()
print("Data in 'todo' table:", rows)

# Insert a new row into the 'todo' table
cursor.execute("INSERT INTO todo (title, description, priority, complete) VALUES ('New Task 3', 'This is a new task3 ', 1, 0);")

# DROP TABLE todo
# cursor.execute("DROP TABLE todo;")

conn.commit()



# Close the connection
conn.close()