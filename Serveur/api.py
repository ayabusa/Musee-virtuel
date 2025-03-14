# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, send_file
from flask import jsonify
import bdd

db = bdd.DB()

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def help():
    return '''
Voilà l'API pour le musée virtuel, tu peux l'utiliser comme suit:</br>
GET /get_couloirs_liste</br>
GET /get_tableaux_from_couloir/&ltcouloir_id&gt</br>
GET /get_tableau_image/&lttableau_id&gt
'''

@app.route('/get_couloirs_liste')
def get_couloirs_liste():
    liste_des_couloirs= {}
    for i in db.recuperer_liste_couloir():
        liste_des_couloirs[i] = db.recuperer_theme_couloir(i)
    return jsonify(liste_des_couloirs)

@app.route('/get_tableaux_from_couloir/<couloir_id>')
def get_tableaux_from_couloir(couloir_id):
    liste_des_tableaux = {}
    for idt in db.recuperer_liste_tableau(couloir_id):
        liste_des_tableaux[idt] = {"nom": db.recuperer_nom_tableau(idt),
                                   "auteur": db.recuperer_auteur_tableau(idt),
                                   "description": db.recuperer_description_tableau(idt),
                                   "date": db.recuperer_date_tableau(idt),
                                   "format": db.recuperer_format_tableau(idt)}
    return jsonify(liste_des_tableaux)

@app.route('/get_tableau_image/<tableau_id>')
def get_tableau_image(tableau_id):
    return send_file("images/tableau_"+str(tableau_id)+".png", mimetype='image/png')

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()