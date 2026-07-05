import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Vérifier les migrations rdv
print("=== Migrations rdv ===")
cursor.execute('SELECT * FROM django_migrations WHERE app="rdv"')
for row in cursor.fetchall():
    print(row)

# Vérifier les tables existantes
print("\n=== Tables existantes ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in cursor.fetchall():
    print(row[0])

conn.close()
