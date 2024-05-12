from flask import Flask, render_template, request, redirect, url_for, Response, session
from flask_mysqldb import MySQL , MySQLdb
from dotenv import load_dotenv
import os
app = Flask(__name__,static_url_path= '/static')
load_dotenv()
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_CURSORCLASS'] = os.getenv("MYSQL_CURSORCLASS")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


mysql = MySQL(app)

# ---- Pagina de Login ---- #
@app.route('/')
def principal():
    return render_template('principal.html')

#----FUNCION DE LOGIN----#
@app.route('/acceso-login', methods=['GET', 'POST'])
def login():
    if 'intentosFallidos' not in session:
        session['intentosFallidos'] = 0
        
    if request.method == 'POST' and 'username' in request.form and 'password':
        _nombre = request.form['username']
        _contraseña = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s and password = %s', (_nombre, _contraseña,))
        account = cur.fetchone()
        if account:
            session['logueado'] = True
            session['id'] = account['id']   
            return data()
        else:
           session['intentosFallidos'] +=1
           if session['intentosFallidos'] >=3:
               return render_template('registrarse.html')
           else:
               return render_template('principal.html')
           
# ---- Si falla 3 veces el ingreso, lo manda al registro ---- #       
def intentos(count):
    if count == 3:
        return register()
   
# ---- Pagina de Registro ---- #
@app.route('/registrarse')
def register():
    return render_template('registrarse.html')    
    
# ---- Añadir Contacto ---- #
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        fechanacimiento = request.form['fechanacimiento']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (email, username, password, fechanacimiento) VALUES (%s,%s,%s,%s)', 
        (email, username, password, fechanacimiento))
        mysql.connection.commit()

    return redirect(url_for('principal'))

# thunder client
# ----SEE PRODUCTS LIST---- #
@app.route('/tabla')
def data():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    print(data)
    
    return render_template('lista.html', productos=data)

# ---- Formulario de ingreso de datos ---- #
@app.route('/anadir')
def anadir():
    return render_template('addproducto.html')

#Funcion para ingresar productos
@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        categoria = request.form['categoria']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (categoria, nombre, precio) VALUES (%s,%s,%s)',
        (categoria, nombre, precio))
        mysql.connection.commit()   
    
    return redirect(url_for('data'))




if __name__ == '__main__':
    app.run(port=5000, debug=True)


##Ejemplo profe con JSON

# @app.route('read')
# def read():
#     cur = mysql.connection.cursor()
#     cur.execute('SELECT * FROM users')
#     data = cur.fetchall()
#     return jsonify(data)    

# @app.route('/add', methods=[ 'POST'])
# def add():
#     datos = request.get_json()
#     print(datos)
#     id = datos.get('id')
#     username = datos.get('username')
#     password = datos.get('password')
#     email = datos.get('email')
#     fechaNacimiento = datos.get('fechaNacimiento')
    
#     cur = mysql.conncetion.cursor()
#     cur.execute('INSERT INTO users (id,username,password,email,fechaNacimiento) VALUE (%s,%s,%s,%s,%s)', 
#     {id,username,password,email,fechaNacimiento})
#     mysql.connection.commit()
   
#     return 'datos recibidos'