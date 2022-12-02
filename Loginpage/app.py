from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from flask_dance.contrib.google import make_google_blueprint, google
from news import *

import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import traceback


import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'
 

 
#create the object of Flask
app  = Flask(__name__)
 
app.config['SECRET_KEY'] = 'Secret Key'
 
blueprint = make_google_blueprint(
    client_id="240639012288-6nf6mpvdsbblc8dmt417b54ufcnm3eqk.apps.googleusercontent.com",
    client_secret="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",
    # reprompt_consent=True,
    offline=True,
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/logins") 

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://exvvlptnrscohn:d6151b341fdd4276a2b25501b033961ca2d554bcc70ef62be7c86d8efc901c7e@ec2-3-219-135-162.compute-1.amazonaws.com:5432/df04t6rqgcmsr3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
 
db = SQLAlchemy(app)
 
 
#login code
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'
 
 
 
 
#This is our model
class UserInfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
 
 
 
    def __init__(self, username, password):
        self.username = username
        self.password = password
 
 
class activitylog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    log = db.Column(db.String(200)) 
    
    def __repr__(self, log):
        self.log = log
        

 
@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))
 
 
 
 
#creating our routes
@app.route('/')
@login_required
def index():
 
    name = current_user.username
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]
    print("Email", email)
    return render_template('index.html', name = name,email = email)
 
 
 
#login route
@app.route('/login' , methods = ['GET', 'POST'])
def Login():
    form = LoginForm()
    hashed_password = generate_password_hash("google", method = 'sha256')
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]

    if request.method == 'POST' and email != None:
        if form.validate_on_submit(): #form.username.data != None and form.password.data != None:
            user = UserInfo.query.filter_by(username=form.username.data).first()

            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
 
                    return redirect(url_for('index'))
 
 
                flash("Invalid Credentials")
    else:
        print(email, " login")
        user = UserInfo.query.filter_by(username=email).first()
        print(user)
        if user:
            print(1)
            if check_password_hash(user.password, hashed_password):
                login_user(user)
                print("in if")
                return redirect(url_for('index'))
        else:
            new_register =UserInfo(username=email, password=hashed_password)
            db.session.add(new_register)
            db.session.commit()
            print("in else")
            return redirect(url_for('index'))
                
 
    return render_template('login.html', form = form)
 
 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('Login'))
 
 
 
#register route
@app.route('/register' , methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
 
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        username = form.username.data
        password = hashed_password
 
 
        new_register =UserInfo(username=username, password=password)
 
        db.session.add(new_register)
 
        db.session.commit()
 
        flash("Registration was successfull, please login")
 
        return redirect(url_for('Login'))
 
 
    return render_template('registration.html', form=form)
 

#news

@app.route('/news/', methods = ['GET', 'POST'])
def news():
    if request.method == 'GET':
        news_list=fetch_top_news()
        # news_list, img =fetch_top_news()
        

    elif request.method == 'POST':
        category =  request.form.get('category')
        print("category: %s"%category)
        if category != None:
            news_list=fetch_category_news(category)
            
        keyword = request.form.get('keyword')
        print("keyword: %s"%keyword)
        if keyword != None:
            news_list=fetch_news_search_topic(keyword)
            
        location = request.form.get('location')
        print("location: %s"%location)
        if location != None:
            news_list= fetch_location_news(location)
               
        print(news_list)
    
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]
    print(email, "/news")
    #return render_template('index.html', newslist = news_list,email = email,img=img)
    return render_template('index.html', newslist = news_list,email = email)
 
@app.route("/logins/google")
def googlelogin():
    print(1)
    hashed_password = "dummy"
    print(hashed_password)
    flag = 0
    print(2)
    if not google.authorized:
        flag = 1
        return render_template(url_for("google.login"))
    print(3)     

    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email=resp.json()["email"]
    print(email)
    if flag != 1:
        try:
            print("inside try")
            new_register =UserInfo(username=email, password=hashed_password)
            db.session.add(new_register)
            db.session.commit() 
        except:
            print("existing user")
    print("123")
    print(email,"login/google")
    return render_template('index.html',email=email)

@app.route('/update', methods = ['POST'])
def update():
    if request.method == 'POST':
        # password ----------------------------------------->
        password = request.form.get('password')
        print(password)

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]
    return render_template('index.html',email = email)
 

@app.after_request
@app.route('/after_request',methods = ['GET'])
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    # log=activitylog(logger.error)
    # db.session.add(log)
    # db.session.commit()
    return response
    return render_template('index.html')
    

@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    return e.status_code

 
#run flask app
if __name__ == "__main__":

    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    logger = logging.getLogger('tdm')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)


    app.run(debug=True)