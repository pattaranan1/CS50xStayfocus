from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

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

# User database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(200), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), unique = True, nullable = False)
    todos = db.relationship('Todo', backref = 'user', lazy = True)

@login_manager.user_loader
def get(id):
    return User.query.get(id)

@app.route('/', methods = ['GET', 'POST'])

#@login_required
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug = True)