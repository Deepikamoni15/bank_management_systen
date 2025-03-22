from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secretkey'

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='bank'
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form['user_type']
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if user_type == 'admin':
            cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
        else:
            cursor.execute("SELECT * FROM customers WHERE username=%s AND password=%s", (username, password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user'] = username
            session['user_type'] = user_type
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'], user_type=session['user_type'])
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'user' in session and session['user_type'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        conn.close()
        return render_template('admin.html', customers=customers)
    return redirect(url_for('login'))

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if 'user' in session and session['user_type'] == 'admin':
        username = request.form['username']
        password = request.form['password']
        balance = request.form['balance']
        
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO customers (username, password, balance) VALUES (%s, %s, %s)", (username, password, balance))
            conn.commit()
        except mysql.connector.IntegrityError:
            conn.rollback()
            return "Error: Username already exists."
        finally:
            conn.close()

        return redirect(url_for('admin'))
    return redirect(url_for('login'))

@app.route('/delete_customer/<int:id>')
def delete_customer(id):
    if 'user' in session and session['user_type'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id=%s", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

@app.route('/customer')
def customer():
    if 'user' in session and session['user_type'] == 'customer':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM customers WHERE username=%s", (session['user'],))
        balance = cursor.fetchone()[0]
        conn.close()
        return render_template('customer.html', balance=balance)
    return redirect(url_for('login'))

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user' in session and session['user_type'] == 'customer':
        amount = float(request.form['amount'])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE customers SET balance = balance + %s WHERE username=%s", (amount, session['user']))
        conn.commit()
        conn.close()
        return redirect(url_for('customer'))
    return redirect(url_for('login'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user' in session and session['user_type'] == 'customer':
        amount = float(request.form['amount'])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM customers WHERE username=%s", (session['user'],))
        balance = cursor.fetchone()[0]
        
        if balance >= amount:
            cursor.execute("UPDATE customers SET balance = balance - %s WHERE username=%s", (amount, session['user']))
            conn.commit()
        conn.close()
        return redirect(url_for('customer'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
