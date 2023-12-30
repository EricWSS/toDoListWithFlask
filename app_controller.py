from flask import Flask, render_template, redirect, url_for, request, session, flash
from forms_controller import *
from db.fuctions_model import UserToDoList 

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/', methods=["GET", "POST"]) #              CRIAÇÃO DE CONTA
def index():
    formulario = CreateAccountForm()
    if formulario.validate_on_submit():
        user = formulario.username.data
        pas = formulario.password.data
        instancia = UserToDoList(user, pas)
        instancia.createUserTable()#ok
        instancia.insertUser()
        instancia.createToDoListTable()
        session['user'] = user
        session['senha'] = pas
        
        return render_template('index.html', form=formulario)
    
    return render_template('index.html', form=formulario)

@app.route('/logon', methods=["GET", "POST"]) # LOGIN
def logon():
    formulario = LogonForm()
    if formulario.validate_on_submit():
        user = formulario.username.data
        pas = formulario.password.data
        instancia = UserToDoList(user, pas)
        instancia.createUserTable()
        if not instancia.userExists():
            flash('Usuário não existe. Cadastre-se.')
            return render_template('logon.html', form=formulario, error="Usuário não existe.")
        session['username'] = user
        session['password'] = pas
        
        return redirect(url_for('logedin'))
    
    return render_template('logon.html', form=formulario)


@app.route('/logedin', methods=["GET", "POST", "DELETE"])
def logedin():
    tasks = []  
    user = session.get('username')
    pas = session.get('password')
    userLoged = str(user)
    if user and pas:
        instancia = UserToDoList(user, pas)
        tasks = instancia.showTasks()
    
    return render_template('logedin.html', tasks=tasks, userLoged=userLoged)

@app.route('/logOff', methods=["GET", "POST"])
def logOff():
    session.pop('username', None)
    session.pop('password', None)
    
    return redirect(url_for('logon'))

@app.route('/delete_task/<int:task_id>', methods=['GET','POST'])
def delete_task(task_id):
    user = session['username']
    pas = session['password']
    if user and pas:
        instancia = UserToDoList(user, pas)
        instancia.deleteTask(task_id)

    return redirect(url_for('logedin'))

@app.route('/insert_task', methods=['POST','GET'])    
def insert_task():
    user = session.get('username')
    pas = session.get('password')
    task_name = request.form.get('taskName') 

    instancia = UserToDoList(user,pas)
    instancia.insertTask(task_name)
    
    return redirect(url_for('logedin'))

if __name__ == '__main__':
    app.run(debug=True)
