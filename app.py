from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

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

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/', methods = ['GET', 'POST'])
@login_required
def main():
    return render_template('main.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Log user in"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # Get username and password
        username = request.form['username']
        password = request.form['password']

        # Ensure username was submitted
        if not username:
            flash("must provide username", "warning")
            return redirect('/login')

        # Ensure password was submitted
        elif not password:
            flash("must provide password", "warning")
            return redirect('/login')

        # Query User from database
        user = User.query.filter_by(username = username).all()

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0].hash, password):
            flash("invalid username and/or password", "danger")
            return redirect('/login')
    
        # User login
        login_user(user[0])

        flash("Logged in successfully.", category = "success")

        return redirect('/')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    """Register user"""
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # Get username, password, and email
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirmation = request.form['confirmation']

        # Ensure username was submitted
        if not username:
            flash("must provide username", "warning")
            return redirect('/register')

        # Ensure password was submitted
        elif not password:
            flash("must provide password", "warning")
            return redirect('/register')

        # Ensure two password fields match
        elif password != confirmation:
            flash("Sorry, your password didn't match", "warning")
            return redirect('/register')

        # Query database for username
        user = User.query.filter_by(username = username).all()

        # Ensure username isn't already taken
        if len(user) == 1:
            flash("Sorry, the username is already taken", "warning")
            return redirect('/register')

        # Query database for email
        user = User.query.filter_by(email = email).all()

        # Ensure username isn't already taken
        if len(user) == 1:
            flash("Sorry, the email is already taken", "warning")
            return redirect('/register')

        # Register user into database
        user = User(username=username, email=email, hash = generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        # Query user from database
        user = User.query.filter_by(username = username).first()

        # User login
        login_user(user)

        return redirect('/')

@app.route('/logout')
def logout():
    """Log user out"""
    logout_user()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug = True)