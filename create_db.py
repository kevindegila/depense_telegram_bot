import sqlite3

# Connexion à la base de données (crée le fichier s'il n'existe pas)
conn = sqlite3.connect('depense.db')

# Création d'un curseur pour exécuter des requêtes
cur = conn.cursor()

# Création de la table
cur.execute('''
    CREATE TABLE depenses (
        id INTEGER PRIMARY KEY,
        designation TEXT,
        categorie TEXT,
        moyen_paiement TEXT,
        montant REAL,
        date DATE
    )
''')

# Enregistrement des modifications
conn.commit()

# Fermeture de la connexion
conn.close()
