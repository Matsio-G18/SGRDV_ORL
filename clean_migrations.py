import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Supprimer les enregistrements de migrations rdv
print("=== Suppression des migrations rdv ===")
cursor.execute('DELETE FROM django_migrations WHERE app="rdv"')
conn.commit()

print("Migrations rdv supprimées")
print("\n=== Migrations rdv restantes ===")
cursor.execute('SELECT * FROM django_migrations WHERE app="rdv"')
for row in cursor.fetchall():
    print(row)

conn.close()
