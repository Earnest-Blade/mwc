CLIENT_ID = 0
CLIENT_SECRET = ''
REDIRECT_URI_SIGNUP = "http://localhost:5000/oauth/signup"
REDIRECT_URI_LOGIN = "http://localhost:5000/oauth/login"

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import website.webutils as webutils
from dataBase import waifuUser

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("baseUI.html",  current_user=current_user,
        title="| Login",
        pagepath="templates/login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    from website.webapp import User, db, app

    user = User.query.filter_by(email=email).first()

    if user.password == "DiscordConnect":
        flash('Connectez-vous via Discord !')
        return redirect(url_for('auth.login'))

    if not user or not check_password_hash(user.password, password):
        flash('Vérifiez vos identifiants...')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)

    return redirect(url_for('main.home'))


@auth.route('/signup')
def signup():
    return render_template("baseUI.html",  current_user=current_user,
        title="| Login",
        pagepath="templates/signup.html")

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    from website.webapp import User, db
    user = User.query.filter_by(name=username).first()
    if user:
        flash('Nom déjà utilisée...')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email déjà utilisée...')
        return redirect(url_for('auth.login'))

    newUser = User(id=User.query.count(), 
            email=email, 
            name=username, 
            password=generate_password_hash(password, method='sha256'),
            link_to_discord=False,
            avatar_URL='https://icon-library.com/images/unknown-person-icon/unknown-person-icon-4.jpg')

    db.session.add(newUser)
    db.session.commit()

    wUser = waifuUser.waifuUser(newUser)
    
    if not waifuUser.userExist(wUser):
        wUser.writeToXML(new=True)

    return redirect(url_for('auth.login'))

@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    return redirect(url_for('main.home'))

@auth.route('/profil')
def profilPage():
    if not current_user.is_authenticated:
        flash("Connectez-vous avant d'accéder à votre page de profil.")
        return redirect(url_for('auth.login'))

    return render_template("baseUI.html",  current_user=current_user, waifuUser=waifuUser.getUserByQuery(current_user.id),
        title="| Login",
        pagepath="templates/profile.html")

# ---- DISCORD LOGIN SYS
@auth.route("/oauth/signup")
def oauth_signup():
    token = webutils.getToken(request.args.get('code'), REDIRECT_URI_SIGNUP)
    userInfo = webutils.getUserInfo(token, '/users/@me')

    from website.webapp import User, db

    user = User.query.filter_by(email=userInfo['email']).first()

    if user:
        flash('Email déjà utilisée...')
        return redirect(url_for('auth.login'))

    avatarURL = webutils.avatar_url(userInfo['avatar'], userInfo['id'])

    newUser = User(id=userInfo['id'], 
            email=userInfo['email'], 
            name=userInfo['username'], 
            password="DiscordConnect",
            link_to_discord=True,
            avatar_URL=avatarURL)

    db.session.add(newUser)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route("/oauth/login")
def oauth_login():
    token = webutils.getToken(request.args.get('code'), REDIRECT_URI_LOGIN)
    userInfo = webutils.getUserInfo(token, '/users/@me')

    from website.webapp import User, db

    user = User.query.filter_by(email=userInfo['email']).first()

    if not user:
        flash('Compte inexistant, créez-vous un compte avec Discord avant de vous connecter avec.')
        return redirect(url_for('auth.singup'))

    login_user(user, remember=True)

    return redirect(url_for('main.home'))
