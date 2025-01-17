drop table IF EXISTS AUTEUR;
drop table IF EXISTS TABLEAUX;
drop table IF EXISTS SALLE;
drop table IF EXISTS NUM_TABLEAU;
drop table IF EXISTS TAGS;

create TABLE AUTEUR(
    id INT PRIMARY KEY,
    nom TEXT
);

create TABLE TAGS(
    tag TEXT PRIMARY KEY
);

CREATE TABLE TABLEAUX(
    id INT PRIMARY KEY,
    titre TEXT,
    auteur_id INT NOT NULL,
    tag_id TEXT,
    salle_id INT,
    format TEXT,
    description TEXT,
    date TEXT,

    FOREIGN KEY (auteur_id) REFERENCES AUTEUR(id),
    FOREIGN KEY (tag_id) REFERENCES TAGS(tag),
    FOREIGN KEY (salle_id) REFERENCES SALLE(id)
);

CREATE TABLE SALLE(
    id INT PRIMARY KEY,
    theme TEXT NOT NULL
);

INSERT into AUTEUR VALUES(1,'jean pierre polanreff');
INSERT into AUTEUR VALUES(2,'zebi la mouche');
INSERT into TAGS VALUES('puant');
INSERT into TABLEAUX VALUES(1,'caca',1,1, 2, "paysage", "un super tableau de fifou", "4/4/2024");
INSERT into TABLEAUX VALUES(2,'prout',1,2, 2, "portrait", "celui là par contre il est guez", "1/1/2027");
INSERT into SALLE VALUES(1,'dechet');
INSERT into SALLE VALUES(2,'wow');
INSERT into SALLE VALUES(3,'incr');




