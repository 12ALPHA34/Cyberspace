from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy data for users and budgets
users = {}
budgets = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
    if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('tracker'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']
        username = session['username']
        if username not in budgets:
            budgets[username] = []
        budgets[username].append({'amount': amount, 'description': description})
    
    user_budgets = budgets.get(session['username'], [])
    return render_template('tracker.html', budgets=user_budgets)

if __name__ == '__main__':
    app.run(debug=True)
