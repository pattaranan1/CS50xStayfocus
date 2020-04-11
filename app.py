from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

# Configure application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stayfocus.db'
app.config['SECRET_KEY'] = 'b$.\xd4\xff\xdb\xdd"\x9d*H-'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Setup Database
db = SQLAlchemy(app)

# Setup login/register
login_manager = LoginManager()
login_manager.init_app(app)

# User Database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    hash = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    todos = db.relationship('Todo', backref = 'user', lazy = True)

# Todo Database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    text = db.Column(db.Text, nullable = False)
    complete = db.Column(db.Boolean, default = False)

@login_manager.user_loader
def get(id):
    return User.query.get(id)

@app.route('/', methods = ['GET', 'POST'])
@login_required
def main():
    return render_template('main.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        login_user(user)
        return redirect('/')

@app.route('/register', methods = ['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirmation = request.form['confirmation']

        user = User(username=username, email=email, hash=password)

        db.session.add(user)
        db.session.commit()
        
        user = User.query.filter_by(username = username).first()
        login_user(user)

        return redirect('/')

@app.route('/logout')
def logout():
    logout_user(current_user)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug = True)