from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flasklogin'
mysql = MySQL(app)


destinations = {
    "paris": {
        "name": "Paris",
        "image": "images/paris.webp",
        "description": "The city of lights and love."
    },
    "tokyo": {
        "name": "Tokyo",
        "image": "images/tokyo.webp",
        "description": "Experience the future and tradition."
    },
    "nairobi": {
        "name": "Nairobi",
        "image": "images/nairobi.png",
        "description": "Explore the heart of Africa."
    },
    "germany": {
        "name": "Germany",
        "image": "images/germany.avif",
        "description": "Dive into ancient history."
    },
    "new-york": {
        "name": "New York City",
        "image": "images/new york.avif",
        "description": "The city that never sleeps."
    },
    "cape-town": {
        "name": "Cape Town",
        "image": "images/cape-town.jpg",
        "description": "Nature's drama and cultural color."
    }
}

@app.route('/')
def home():
    return redirect(url_for('login'))  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            flash('Username already exists. Please choose another.', 'danger')
            cursor.close()
            return redirect(url_for('register'))  
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            mysql.connection.commit()
            cursor.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login')) 

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[2] == password:
            session['username'] = username
            return redirect(url_for('index'))  
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login')) 
    return render_template('login.html')

@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

@app.route('/book', methods=['POST'])
def book():
    from_city = request.form['from_city']
    to_city = request.form['to_city']
    date = request.form['date']

    price = 150 if from_city.lower() != to_city.lower() else 100


    return redirect(url_for('seats', from_city=from_city, to_city=to_city, date=date, price=price))

@app.route('/seats')
def seats():
    from_city = request.args.get('from_city')
    to_city = request.args.get('to_city')
    date = request.args.get('date')
    price = request.args.get('price')

    return render_template('seats.html', from_city=from_city, to_city=to_city, date=date, price=price)

@app.route('/confirm', methods=['POST'])
def confirm():
   
    session['booking'] = {
        'from_city': request.form['from_city'],
        'to_city': request.form['to_city'],
        'date': request.form['date'],
        'seat': request.form['seat'],
        'price': request.form['price']
    }
    return redirect(url_for('confirm_get'))

@app.route('/confirm_get')
def confirm_get():
    data = session.get('booking')
    if not data:
        flash('No booking data found.', 'warning')
        return redirect(url_for('index'))

    return render_template('confirm.html', **data)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':

        flash('Payment successful!', 'success')
        return redirect(url_for('ticket_get'))

    return render_template('payment.html')

@app.route('/ticket', methods=['POST'])
def ticket():

    session['ticket'] = {
        'from_city': request.form['from_city'],
        'to_city': request.form['to_city'],
        'date': request.form['date'],
        'seat': request.form['seat'],
        'price': request.form['price']
    }
    return redirect(url_for('ticket_get'))

@app.route('/ticket_get')
def ticket_get():
    data = session.get('ticket')
    if not data:
        flash('No ticket data found.', 'warning')
        return redirect(url_for('index'))

    return render_template('ticket.html', **data)

@app.route('/destination/<name>')
def destination_detail(name):
    dest = destinations.get(name)
    if not dest:
        return "Destination not found", 404
    return render_template('details.html', dest=dest)

if __name__ == '__main__':
    app.run(debug=True)
