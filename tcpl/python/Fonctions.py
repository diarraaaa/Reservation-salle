#importer toutes les classes dont on a besoin depuis le framework
from flask import Flask, jsonify, render_template, request,session, redirect
import os
from flask import url_for
#importer le connecteur pour se connecter à notre base Mysql
import mysql.connector
import re
app = Flask(__name__)
#fonction pour se connecter à notre base de données
def connectdatabase():
    return mysql.connector.connect(
    host='localhost',
    user='diarra',
    password='passer',
    database='tcpl'
    )


def nettoyer_nom_fichier(nom_fichier):
    # Remplacer les caractères spéciaux par des tirets
    nom_fichier_nettoye = re.sub(r'[^\w.-]', '-', nom_fichier)
    return nom_fichier_nettoye

#fonction pour s'inscrire sur le site
def add_client():
    connectdatabase()
    try:
            #on récupére les informations à partir du foemulaire
            nom=request.form['nom']
            prenom=request.form['prenom']
            username=request.form['username']
            email=request.form['email']
            password=request.form['password']
            #créer une variable de connexion
            conn=connectdatabase()
            #creér un curseur qui nous permet d'éxecuter des requétes sql
            curseur=conn.cursor()
            #verifier si le mail a déja été utilisé
            verification_email="Select * from client where email=%s"
            curseur.execute(verification_email,(email,))
            email_present=curseur.fetchone()
            #vérifier si le username est déja pris
            verification_username="Select * from client where username=%s"
            curseur.execute(verification_username,(username,))
            username_present=curseur.fetchone()
            #afficher des messages d'avertissement
            if email_present:
                error_message = 'Email deja utilisé '
                return render_template('Inscription.html', error_message=error_message)
            
            if username_present:
                error_message = "Nom d'utilisateur non disponible"
                return render_template('Inscription.html', error_message=error_message)


            #si il n'y pas de problémes,on ajoute le client à la base
            requete="INSERT INTO client(nom, prenom, username, email, password) VALUES (%s, %s, %s, %s, %s)"
            VALUES=(nom, prenom, username, email, password)
            curseur.execute(requete,VALUES)
            conn.commit()
            curseur.close()
            conn.close()
            #afficher un message de succés
            success_message = 'Inscription réuissie'
            return render_template('Inscription.html', success_message=success_message)
    #gerer les erreurs
    except mysql.connector.Error as errorconn:
          return jsonify({'error': str(errorconn)})
    except KeyError:
        return jsonify({'error': 'Missing required fields'})
    
def connect_client():
     connectdatabase()
     try:
            username=request.form['username']
            password=request.form['password']
            conn=connectdatabase()
            curseur=conn.cursor()
            #verifier si il est présent dans la base
            verification_client="Select * from client where username=%s and password=%s "
            curseur.execute(verification_client,(username,password))
            user_present=curseur.fetchone()

            #afficher ds messages en fonction de sa présence ou non
            if  user_present:
                 session['username']=username
                 return timeline_client()
            else:
                error_message = 'Informations érronnées'
                return render_template('Connexion.html', error_message=error_message)
                 
            #gerer les erreurs
     except mysql.connector.Error as errorconn:
          return jsonify({'error': str(errorconn)})
     except KeyError:
        return jsonify({'error': 'Missing required fields'})
     
def modifier_profil():
    connectdatabase()
    try:     
        conn=connectdatabase()
        curseur=conn.cursor()
        username=session.get('username')
        newpassword=request.form["newpass"]

        #changer le mot de passe
        changer_mot_de_passe="Update client set password=%s where username=%s"
        curseur.execute(changer_mot_de_passe,(newpassword,username))

        conn.commit()

        #afficher ds messages en fonction de la réuissite ou pas
        if  curseur.rowcount>0:
             success_message = 'Changement réuissi'
             return render_template('Profil.html', success_message=success_message)
            
        else:
             error_message = 'Changement non réuissi'
             return render_template('Profil.html', error_message=error_message)
                 
         #gerer les erreurs
    except mysql.connector.Error as errorconn:
        return jsonify({'error': str(errorconn)})
    except KeyError:
        return jsonify({'error': 'Missing required fields'})
    
def timeline_client():
     sess_username=session.get('username')
     connectdatabase()
     conn=connectdatabase()
     curseur=conn.cursor()
     curseur.execute("Select * from Salles")
     salles=curseur.fetchall()
     conn.commit()
     curseur.close()
     conn.close()
     return render_template('Timeline.html',sess_username=sess_username,salles=salles)

def ajouter_salle():
     connectdatabase()
     #definir le repertoire des images
     repertoire='python/static/images'
     #receuillir toutes les informations
     nom=request.form['nom']
     prix=request.form['prix']
     capacite=request.form['capacite']
     adresse=request.form['adresse']
     description=request.form['description']
     disponibilite=request.form['option-disponibilité']
     type_salle=request.form['type-salle']
     photo1=request.files['photo1']
     photo2=request.files['photo2']
     #verifier les extensions des fichiers qui ont été soumis
     if photo1.filename.endswith('png') or photo1.filename.endswith('jpeg') :
          photo1_filename = photo1.filename
          #si c'est le cas on nettoie le nom du fichier avec la fonction
          photo1_filename=nettoyer_nom_fichier(photo1_filename)
          if not os.path.exists(repertoire):
           os.makedirs(repertoire)
          #on enregistre le fichier dans notre repertoire
          photo1.save(os.path.join(repertoire,photo1_filename))
          #on récupére le chemin de l'image
          chemin1=os.path.join('static/images',photo1_filename)
     else:
          errorphoto1="Format photo 1 non acceptée"
          return render_template("AjoutSalle.html",errorphoto1=errorphoto1)
     
     if photo2.filename.endswith('png') or photo2.filename.endswith('jpeg') :
          photo2_filename = photo2.filename
          photo2_filename=nettoyer_nom_fichier(photo2_filename)
          if not os.path.exists(repertoire):
           os.makedirs(repertoire)
          photo2.save(os.path.join(repertoire,photo2_filename))
          chemin2=os.path.join('/static/images',photo2_filename)
     else:
          errorphoto2="Format photo 2 non acceptée"
          return render_template("AjoutSalle.html",errorphoto2=errorphoto2)

     try:
        conn=connectdatabase()
        curseur=conn.cursor()
        requete='Insert into Salles(nom,prix,capacite,adresse,description,disponibilite,type_salle,photo1,photo2)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values=(nom,prix,capacite,adresse,description,disponibilite,type_salle,chemin1,chemin2)
        curseur.execute(requete,values)
        conn.commit()
        curseur.close()
        conn.close()
        success_message='Salle ajoutée'
        return render_template("AjoutSalle.html",success_message=success_message)
     except mysql.connector.Error as errorconn:
          return jsonify({'error': str(errorconn)})
     except KeyError:
        return jsonify({'error': 'Missing required fields'})
     
def AfficherInfoSalle():
   connectdatabase()
   conn=connectdatabase()
   curseur=conn.cursor()
   id=request.form['id']
   requete="Select * from Salles where id=%s"
   curseur.execute(requete,(id,))
   detail=curseur.fetchall()
   conn.commit()
   curseur.close()
   conn.close()
   return render_template("InfoSalle.html",detail=detail)

if __name__ == '__main__':
    app.run(debug=True)
