import sqlite3
import string
import random

# Connexion à la base de données (elle se crée toute seule)
def init_db():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  short_code TEXT UNIQUE, 
                  long_url TEXT, 
                  clicks INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()