from flask import Flask, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash




app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataSP.db'
db= SQLAlchemy(app)
app.config['SECRET_KEY'] = 'House010203'

class Users(db.Model):       
    id= db.Column(db.Integer, primary_key= True)
    username= db.Column(db.String(200), 
                   nullable= False, 
                   unique= True)
    
    password_hash= db.Column(db.String(200), nullable= False)         
    date_created= db.Column(db.DateTime, default= datetime.utcnow)


@app.route('/')
def index():
    return render_template('webSP.html')
    

@app.route('/register', methods= ['POST', 'GET'])
def botones():

    if 'student' in request.form:
        session['tipo_usuario'] = 'student'

    elif 'teacher' in request.form: 
        session['tipo_usuario'] = 'teacher'

    return render_template('register.html')



@app.route('/login', methods= ['POST', 'GET'])
def enter():

    tipo= session.get('tipo_usuario')

    if tipo == 'student':

        return render_template('schedule1.html')

    elif tipo == 'teacher':
        return render_template('schedule2.html')

    else:
        return 'Error', 401


@app.route('/inputs', methods= ['POST', 'GET'])
def login():

    if request.method == 'POST':

        username= request.form.get('usuario', '').strip()
        password= request.form.get('password', '')

        uss= Users.query.filter_by(username=username).first()

        if uss:

            if check_password_hash(uss.password_hash, password):
                session['uss_id'] = uss.id
                return redirect(url_for('index'))

            else:
                return 'Contraseña incorrecta', 401

        else:
            new_uss= Users(
                username=username,
                password_hash= generate_password_hash(password)
            )

            db.session.add(new_uss)
            db.session.commit()

            session['uss_id'] = new_uss.id
            return redirect(url_for('index'))
        
    return render_template('register.html')


if __name__== '__main__':
    with app.app_context():
        db.create_all()

    app.run(
        host= '0.0.0.0',
        port= 5000,
        debug= True)    