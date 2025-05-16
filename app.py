from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables
load_dotenv()

# Flask setup
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')
app.config['DATABASE'] = os.environ.get('DATABASE_PATH', 'cafe.db')

# Reusable DB connection
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products', methods=['GET', 'POST'])
def products():
    conn = get_db_connection()
    cursor = conn.cursor()
    search_term = request.args.get('search', '')

    if search_term:
        cursor.execute('''
            SELECT * FROM products
            WHERE name LIKE ? OR description LIKE ?
        ''', ('%' + search_term + '%', '%' + search_term + '%'))
    else:
        cursor.execute('SELECT * FROM products')

    items = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=items, search_term=search_term)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dish = request.form['dish']
        message = request.form['message']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (name, email, dish, message)
            VALUES (?, ?, ?, ?)
        ''', (name, email, dish, message))
        conn.commit()
        conn.close()

        return render_template('form.html', submitted=True)

    return render_template('form.html', submitted=False)

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form['name']
    item = request.form['item']
    quantity = request.form['quantity']
    notes = request.form.get('notes', '')
    email = session.get('user_email', None)

    if not email:
        flash("⚠️ You must be logged in to place an order as a member.", "error")
        return redirect(url_for('account'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (name, item, quantity, notes, email)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, item, quantity, notes, email))
    conn.commit()
    conn.close()

    flash('✅ Order submitted successfully!', 'success')
    return redirect(url_for('order'))

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        if 'login_email' in request.form:
            email = request.form['login_email']
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE email = ?', (email,))
            account_info = cursor.fetchone()
            conn.close()

            if account_info:
                session['user_email'] = email
                return redirect(url_for('account'))
            else:
                flash('❌ No account found with that email.', 'error')
                return redirect(url_for('account'))

    email = session.get('user_email', None)
    if not email:
        return render_template('login.html')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE email = ? ORDER BY id DESC', (email,))
    orders = cursor.fetchall()
    cursor.execute('SELECT * FROM accounts WHERE email = ?', (email,))
    account_info = cursor.fetchone()
    conn.close()

    return render_template('account.html', orders=orders, account_info=account_info)

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('👋 You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (username, email, phone)
            VALUES (?, ?, ?)
        ''', (name, email, phone))
        conn.commit()
        conn.close()

        flash("✅ Account created successfully! Please log in.", "success")
        return redirect(url_for('account'))

    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE email = ?', (email,))
        account = cursor.fetchone()
        conn.close()

        if account:
            session['user_email'] = email
            flash('✅ Logged in successfully!', 'success')
            return redirect(url_for('account'))
        else:
            flash('❌ No account found with that email.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(debug=True, port=port)
