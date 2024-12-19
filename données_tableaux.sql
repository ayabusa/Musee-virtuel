drop table AUTEUR;
drop table TABLEAUX;
drop table SALLE;
drop table NUM_TABLEAU;
drop table TAGS;

create TABLE AUTEUR(
    nom TEXT PRIMARY KEY
);

create TABLE TAGS(
    tag TEXT PRIMARY KEY
);

CREATE TABLE TABLEAUX(
    titre PRIMARY KEY,
    auteur_id INT NOT NULL,
    tag_id TEXT,

    FOREIGN KEY (auteur_id) REFERENCES AUTEUR(nom),
    FOREIGN KEY (tag_id) REFERENCES TAGS(tag)
);

CREATE TABLE SALLE(
    ID INT PRIMARY KEY,
    thème TEXT NOT NULL
);

CREATE TABLE NUM_TABLEAU(
    num INT PRIMARY KEY,
    IDT INT NOT NULL,
    IDS INT NOT NULL,
    FOREIGN KEY (IDT) REFERENCES TABLEAUX(titre),
    FOREIGN KEY (IDS) REFERENCES SALLE(ID)
);

INSERT into AUTEUR VALUES('jean pierre polanreff');
INSERT into TAGS VALUES('puant');
INSERT into TABLEAUX VALUES('caca',1,1);
INSERT into SALLE VALUES(1,'dechet');
INSERT into NUM_TABLEAU VALUES(1,'caca',1);




