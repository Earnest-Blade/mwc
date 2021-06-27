from flask import Flask, render_template, request, session, flash, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
import sys, re, os
sys.path.append("d:\\Projets\\Code\\Python\\WaifuBot\\")

from website.webauth import auth as auth_blueprint
from website.webmain import main as main_blueprint

import website.webclass as webclass
from dataBase import waifuSerie

db = SQLAlchemy()
app = Flask(__name__, template_folder="webfiles", static_folder="webfiles")

# Fonction créant l'app Flask
def createApp():    
    app.secret_key = os.urandom(12)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def loadUser(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    

    webclass.loadAllPosts()

    return app

############# CLASS

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    link_to_discord = db.Column(db.Boolean())
    avatar_URL = db.Column(db.String(100))

if __name__ == "__main__":
    waifuSerie.createAllSeriesFromXMLFile()
    createApp().run(debug=True)