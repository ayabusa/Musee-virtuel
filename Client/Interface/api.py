import urllib.request, json, pygame, os

try:
    os.mkdir("tmp")
except:
    print("tmp already exist")
address = "http://localhost:5000"
def get_couloir_liste()->dict:
    """Retourne un dictionnaire ayant pour cle l'id du couloir et pour valeur son nom/theme
    ex: {1: 'couloir de fifou', 2: 'couloir chiant'}
    La fonction retourne None si il y a une erreure"""
    contents = urllib.request.urlopen(address+"/get_couloirs_liste").read()
    try:
        tmp = json.loads(contents)
        res = {}
        for i in tmp:
            res[int(i)] = tmp[i]
        return res
    except:
        return None

def get_tableaux_from_couloir_id(id: int)->dict:
    """Retourne un dictionnaire de dictionnaire ayant pour cle l'id du tableau et pour valeur un dictionnaire avec chaque info
    ```
    ex:
    {
        1: {'auteur': 'jean pierre polanreff', 'date': '4/4/2024', 'description': 'un super tableau de fifou', 'format': 'paysage', 'nom': 'caca'},
        2: {'auteur': 'zebi la mouche', 'date': '1/1/2027', 'description': 'celui lÃ\xa0 par contre il est guez', 'format': 'portrait', 'nom': 'prout'}
    }
    ```
    La fonction retourne None si il y a une erreure"""
    contents = urllib.request.urlopen(address+"/get_tableaux_from_couloir/"+str(id)).read()
    try:
        tmp = json.loads(contents)
        res = {}
        for i in tmp:
            res[int(i)] = tmp[i]
        return res
    except:
        return None

def get_tableau_image(tableau_id:int)->object:
    """Retourne l'image avec l'id specifie sous la forme d'un ..."""

    f = open('tmp/img'+str(tableau_id)+'.png','wb+')
    f.write(urllib.request.urlopen(address+"/get_tableau_image/"+str(tableau_id)).read())
    f.close()
    return pygame.image.load('./tmp/img'+str(tableau_id)+'.png')

# Pour tester si tout marche
"""
print(get_couloir_liste())
print(get_tableaux_from_couloir_id(2))
"""
