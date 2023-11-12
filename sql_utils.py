import json
import sqlite3
from datetime import datetime


def save_to_sql(data, db_file="depense.db"):
    
    data = json.loads(data)
    data['date'] = datetime.today().strftime("%Y-%m-%d")

    
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Insert data into the 'depenses' table
    insert_query = """INSERT INTO depenses (designation, moyen_paiement, categorie, montant, date)
                    VALUES (?, ?, ?, ?, ?)"""

    cursor.execute(insert_query, (data["designation"], data["moyen_paiement"], data["categorie"], data["montant"], data["date"]))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    

def execute_query(sql_query, db_file='depense.db'):

    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(sql_query)
    result = cursor.fetchall()

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return result