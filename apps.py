from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret123'

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

# Create DB
with app.app_context():
    db.create_all()

# Home (Login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        check = User.query.filter_by(username=user, password=pwd).first()
        if check:
            session['user'] = user
            return redirect('/dashboard')
        else:
            return "Invalid Credentials"

    return render_template('login.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        new_user = User(username=user, password=pwd)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/')

    return render_template('signup.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
