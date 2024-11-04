from flask import Flask, render_template
from python import app
from python.Fonctions import add_client
from python.Fonctions import connect_client
from python.Fonctions import modifier_profil,timeline_client,ajouter_salle,AfficherInfoSalle

@app.route('/')
def index():
    return render_template('Acceuil.html')

@app.route('/Connexion')
def Connexion():
    return render_template('Connexion.html')

@app.route('/Inscription')
def Inscription():
    return render_template('Inscription.html')

@app.route('/Profil')
def Profil():
    return render_template('Profil.html')

@app.route('/ajout_client', methods=['POST'])
def Ajouter_client_route():
     return add_client()

@app.route('/seconnecter', methods=['POST'])
def Seconnecter_route():
     return connect_client()


@app.route('/modifierprofil', methods=['POST'])
def ModifierProfil_route():
    return modifier_profil()

@app.route('/ajout_salle', methods=['POST'])
def AjoutSalle_route():
    return ajouter_salle()

@app.route('/AjoutAdmin')
def AjoutAdmin_route():
    return render_template('AjoutSalle.html')

@app.route('/InfoSalle',methods=['POST'])
def InfoSalle_route():
    return AfficherInfoSalle()

@app.route('/timeline')
def timeline_route():
    return timeline_client()
     
    
if __name__ == '__main__':
    app.run(debug=True)
