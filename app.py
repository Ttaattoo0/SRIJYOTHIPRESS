from flask import Flask, render_template, request, redirect, flash
import pymysql
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'supersecret'  #  Change this to something secure in production

#  Database connection
def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor  # Makes fetched data easier to work with
    )

# Routes
@app.route('/')
def home():
    return render_template('index.html', page='home')

@app.route('/about')
def about():
    return render_template('about.html', page='about')

@app.route('/services')
def services():
    return render_template('services.html', page='services')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', page='gallery')

@app.route('/quote', methods=['GET', 'POST'])
def quote():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        details = request.form.get('details')

        if name and email and details:
            connection = get_db_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO quotes (name, email, phone, details) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (name, email, phone, details))
                    connection.commit()
            flash(' Quote request submitted successfully!', 'success')
        else:
            flash(' All fields are required.', 'error')

        return redirect('/quote')

    return render_template('quote.html', page='quote')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            connection = get_db_connection()
            with connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (name, email, message))
                    connection.commit()
            flash(' Message sent successfully!', 'success')
        else:
            flash(' Please fill out all fields.', 'error')

        return redirect('/contact')

    return render_template('contact.html', page='contact')

@app.route('/admin')
def admin():
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM quotes ORDER BY id DESC")
            quotes = cursor.fetchall()
            cursor.execute("SELECT * FROM messages ORDER BY id DESC")
            messages = cursor.fetchall()

    return render_template('admin.html', quotes=quotes, messages=messages, page='admin')

# Start app
if __name__ == '__main__':
    app.run(debug=True)
