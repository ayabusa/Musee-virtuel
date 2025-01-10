import sqlite3

with open('bdd.sql', 'r') as sql_file:
    sql_script = sql_file.read()

con = sqlite3.connect("../bdd.db")
cur = con.cursor()
cur.executescript(sql_script)

def recuperer_liste_couloir()->list:
    # Renvoie une liste des id de tout les couloirs
    res = cur.execute("SELECT id FROM SALLE")
    return [i[0] for i in res.fetchall()]

def recuperer_theme_couloir(couloir_id: int)->str:
    # Renvoie le thème du couloir à partir de son id
    res = cur.execute("SELECT theme FROM SALLE WHERE ID=?",(couloir_id,))
    return res.fetchone()[0]

def recuperer_liste_tableau(couloir_id: int)->list:
    # Renvoie une liste des id des tableaux appartenant a un couloir
    res = cur.execute("SELECT id FROM TABLEAUX WHERE salle_id=?",(couloir_id,))
    return [i[0] for i in res.fetchall()]

def recuperer_nom_tableau(tableau_id: int)->str:
    # Renvoie le nom du tableau à partir de son id
    res = cur.execute("SELECT titre FROM TABLEAUX WHERE id=?",(tableau_id,))
    return res.fetchone()[0]

def recuperer_auteur_tableau(tableau_id: int)->str:
    # Renvoie l'auteur du tableau à partir de son id
    res = cur.execute("SELECT nom FROM TABLEAUX JOIN AUTEUR ON TABLEAUX.id=AUTEUR.id WHERE TABLEAUX.id=?",(tableau_id,))
    return res.fetchone()[0]

def recuperer_description_tableau(tableau_id: int)->str:
    # Renvoie la description du tableau à partir de son id
    # A faire
    pass

def recuperer_date_tableau(tableau_id: int)->str:
    # Renvoie la date du tableau à partir de son id
    # A faire
    pass

print(recuperer_liste_tableau(2))
print(recuperer_auteur_tableau(1))
print(recuperer_auteur_tableau(2))