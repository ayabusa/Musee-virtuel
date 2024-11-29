# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flask import jsonify
import bdd

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

@app.route('/get_couloirs_liste')
def get_couloirs_liste():
    liste_des_couloirs = {1: "de",2: "dqzd",3: "dqzdq"}
    for i in bdd.recuperer_liste_couloir():
        liste_des_couloirs[i] = bdd.recuperer_theme_couloir(i)
    return jsonify(liste_des_couloirs)

@app.route('/get_tableaux_from_couloir/<couloir_id>')
def get_tableaux_from_couloir(couloir_id):
    liste_des_tableaux = {1: ["nom", "auteur_id", "tags", "descriptionn", "date"], 2: ["nom", "auteur_id", "tags", "descriptionn", "date"]}
    for idt in bdd.recuperer_liste_tableau(couloir_id):
        liste_des_tableaux[idt] = [bdd.recuperer_nom_tableau(idt),
                                   bdd.recuperer_auteur_tableau(idt),
                                   bdd.recuperer_description_tableau(idt),
                                   bdd.recuperer_date_tableau(idt)]
    return jsonify(liste_des_tableaux)


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()