from flask import Flask, render_template, flash, request, redirect, url_for
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from news import *
 
#create the object of Flask
app  = Flask(__name__)
 
app.config['SECRET_KEY'] = 'Secret Key'
 
 
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
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
 
 
 
 
@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))
 
 
 
 
#creating our routes
@app.route('/')
@login_required
def index():
 
    name = current_user.username
 
    return render_template('index.html', name = name)
 
 
 
#login route
@app.route('/login' , methods = ['GET', 'POST'])
def Login():
    form = LoginForm()
 
    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(username=form.username.data).first()
 
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
 
                    return redirect(url_for('index'))
 
 
                flash("Invalid Credentials")
 
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

@app.route('/news/')
def news():
    # modify here
    news_list=fetch_top_news()#fetchcategorynews(cat)
    return render_template('news.html', newslist = news_list)
 

 
 
 
#run flask app
if __name__ == "__main__":
    app.run(debug=True)