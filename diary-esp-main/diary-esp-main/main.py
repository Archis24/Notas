# Importar
from flask import Flask, render_template,request, redirect
# Conectando a la biblioteca de bases de datos
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Conectando SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creando una base de datos
db = SQLAlchemy(app)
# Creación de una tabla

class Card(db.Model):
    # Creación de columnas
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Título
    title = db.Column(db.String(100), nullable=False)
    # Descripción
    subtitle = db.Column(db.String(300), nullable=False)
    # Texto
    text = db.Column(db.Text, nullable=False)

    # Salida del objeto y del id
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Asignación #2. Crear la tabla Usuario
class User(db.Model):
    # Creación de las columnas
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Correo
    login = db.Column(db.String(100), nullable=False)
    # Contraseña
    password = db.Column(db.String(100), nullable=False)
    








# Creamos una ruta para la página de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        # Obtenemos el nombre de usuario y la contraseña del formulario
        form_login = request.form['email']
        form_password = request.form['password']
        
        # Buscamos todos los usuarios en la base de datos
        users_db = User.query.all()
        for user in users_db:
            # Comprobamos si el nombre de usuario y la contraseña son correctos
            if form_login == user.login and form_password == user.password:
                return redirect('/index')
        else:
            # Si no son correctos, mostramos un mensaje de error
            error = 'Nombre de usuario o contraseña incorrectos'
        return render_template('login.html', error=error)
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login= request.form['email']
        password = request.form['password']
        
        #Asignación #3. Hacer que los datos del usuario se registren en la base de datos.
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


# Ejecutar la página de contenidos
@app.route('/index')
def index():
    # Visualización de las entradas de la base de datos
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Ejecutar la página con la entrada
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Ejecutar la página de creación de entradas
@app.route('/create')
def create():
    return render_template('create_card.html')

# El formulario de inscripción
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Creación de un objeto que se enviará a la base de datos
        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')





if __name__ == "__main__":
    app.run(debug=True)
