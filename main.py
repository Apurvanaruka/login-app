from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import app


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secret key for your application

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Function to initialize the database
def init_db():
    with app.app_context():
        db.create_all()


# Route to render the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username
            return render_template('dashborad.html')
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

# Route to render the dashboard page
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# Route to handle logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Route to render the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists!'

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return 'User created successfully!'

    return render_template('signup.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
