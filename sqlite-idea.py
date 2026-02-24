import sqlite3

# This creates a local file named 'code_data.db'
conn = sqlite3.connect("code_data.db")
cursor = conn.cursor()

# Create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        language TEXT,
        code_content TEXT,
        intent_description TEXT
    )
""")

# Insert a code snippet
code_snippet = "def hello(): print('world')"
cursor.execute(
    "INSERT INTO code_entities (name, language, code_content) VALUES (?, ?, ?)",
    ("hello_world", "python", code_snippet),
)

conn.commit()
conn.close()
