import sqlite3

class DB:
    def __init__(self):
        with open('bdd.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        self.con = sqlite3.connect("bdd.db")
        self.cur = self.con.cursor()
        self.cur.executescript(sql_script)
        self.con.commit()
    def recuperer_liste_couloir(self)->list:
        # Renvoie une liste des id de tout les couloirs
        res = self.cur.execute("SELECT id FROM SALLE")
        return [i[0] for i in res.fetchall()]

    def recuperer_theme_couloir(self,couloir_id: int)->str:
        # Renvoie le thème du couloir à partir de son id
        res = self.cur.execute("SELECT theme FROM SALLE WHERE ID=?",(couloir_id,))
        return res.fetchone()[0]

    def recuperer_liste_tableau(self,couloir_id: int)->list:
        # Renvoie une liste des id des tableaux appartenant a un couloir
        res = self.cur.execute("SELECT id FROM TABLEAUX WHERE salle_id=?",(couloir_id,))
        return [i[0] for i in res.fetchall()]

    def recuperer_nom_tableau(self,tableau_id: int)->str:
        # Renvoie le nom du tableau à partir de son id
        res = self.cur.execute("SELECT titre FROM TABLEAUX WHERE id=?",(tableau_id,))
        return res.fetchone()[0]

    def recuperer_auteur_tableau(self,tableau_id: int)->str:
        # Renvoie l'auteur du tableau à partir de son id
        res = self.cur.execute("SELECT nom FROM TABLEAUX JOIN AUTEUR ON TABLEAUX.id=AUTEUR.id WHERE TABLEAUX.id=?",(tableau_id,))
        return res.fetchone()[0]

    def recuperer_format_tableau(self,tableau_id: int)->str:
        # Renvoie le format (paysage, portrait ou carré)
        res = self.cur.execute("SELECT format FROM TABLEAUX WHERE id=?",(tableau_id,))
        return res.fetchone()[0]

    def recuperer_description_tableau(self,tableau_id: int)->str:
        # Renvoie la description du tableau à partir de son id
        res = self.cur.execute("SELECT description FROM TABLEAUX WHERE id=?",(tableau_id,))
        return res.fetchone()[0]

    def recuperer_date_tableau(self,tableau_id: int)->str:
        # Renvoie la date du tableau à partir de son id
        res = self.cur.execute("SELECT date FROM TABLEAUX WHERE id=?",(tableau_id,))
        return res.fetchone()[0]