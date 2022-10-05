from flask import Flask, render_template,\
    request,redirect,make_response
from flask import url_for,json, jsonify
from flask import session,abort,flash
from wtforms import *
import click
import os
from forms import LoginForm, NoteForm, EditForm

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_folder='errors')
app.secret_key = 'secrete string'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('DATABASE_URL','sqlite:///'+os.path.join(app.root_path,'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False


class Note(db.Model):
    __tablename__ = 'notes_db'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)

@app.before_request
def before():
    print("request received and begin to process ... ")

@app.route('/')
def index():
    # return render_template('index.html')
    if session.get('logged_in') :
        return "<h1> User has already logged in <h1>"
    else:
        return render_template("index.html")

@app.route('/login')
def login():
    session['logged_in'] = True
    print(session.get('logged_in'))
    return request.referrer
    # return redirect(url_for('greet',name = 'aure'))


@app.route('/hi/<name>')
def hi(name):
    return redirect(url_for('greet',name=name))

@app.route('/newpage')
def newpage():
    return '<p> this is a new page <p> <'


@app.route('/hello/<name>',methods = ['GET','POST'])
def greet(name):
    return 'Hello {}'.format(name),201

@app.route('/hello1')
def hello1():
    name = request.args.get('name','Flask') # default = 'Flask'
    return 'hello {}'.format(name)

@app.route('/goback/<int:year>')
def goback(year):
    return 'welcome to {}'.format(2022-year)

@app.route('/colors/<any(red,yellow,blue):color>')
def color(color):
    return 'I love {}'.format(color)

@app.route('/redir')
def redir():
    # return '',302,{'Location':'http://www.baidu.com'} # redirect to baidu
    return redirect('http://www.baidu.com')


@app.route('/try_cookie')
def try_cookie():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name','Human') # default is 'Human'
    return '<h1> hello cookie {} <h1>'.format(name)

@app.route('/hello')
def hello():
    name = request.args.get('name')
    if not name :
        name = request.cookies.get('name','Human')
        response = '<h1> hello cookie {} <h1>'.format(name)
    if session.get('logged_in'):
        response += '[Authenticated]'
        session.pop('logged_in')
    else:
        abort(403)
    return response


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('try_cookie')))
    response.set_cookie('name',name)
    return response


@app.route('/foo')
def foo():
    response = make_response('hello foo')
    response.mimetype = 'text/plain'
    return response

@app.route('/foo2')
def foo2():
    data = {
        'name' : 'david',
        'age' : '20'
    }
    response = make_response(json.dumps(data))
    response.mimetype='application/json'
    return response

@app.route('/foo3')
def foo3():
    return jsonify({'name':'david', 'age':'20'})

@app.route('/helper')
def helper():
    print(request.args)
    username = request.args.get('username')
    pwd = request.args.get('password')
    return redirect("http://127.0.0.1:8000/hello/{}".format(username))

@app.route('/flash')
def flash_message():
    flash("I'm a flash message")
    flash("second flash message")
    return redirect(url_for('greet',name="Aure"))

@app.route('/base')
def getbase():
    return render_template('base.html')

@app.route('/basic', methods=['GET','POST'])
def basic():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        print(username)
        flash("Welcome {}".format(username))
        return redirect(url_for('index'))
    return render_template("basic.html",form = form)

@app.route('/newnote', methods=['GET','POST'])
def newNote():
    noteForm = NoteForm()
    if noteForm.validate_on_submit():
        print('success')
        body = noteForm.body.data
        note = Note(body = body)
        db.session.add(note)
        db.session.commit()
        flash("your note is saved")
        return redirect(url_for('notes'))
    return render_template('new_note.html',form=noteForm)

@app.route('/notes')
def notes():
    notes = Note.query.all()
    return render_template('notes.html',notes=notes)

@app.route('/edit_note/<int:note_id>',methods=['GET','POST'])
def edit_note(note_id):
    editForm = EditForm()
    note = Note.query.get(note_id)
    if editForm.validate_on_submit():
        note.body = editForm.body.data
        db.session.commit()
        flash("Your note is updated!")
        return redirect(url_for('notes'))

    editForm.body.data = note.body
    return render_template('edit_note.html',form=editForm,note=note)

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    flash("you note is deleted")
    # return redirect(url_for('notes'))
    return redirect(request.referrer) #返回上一层


@app.errorhandler(404)
def page_not_found(err):
    return render_template('errors/404.html'),404

@app.cli.command()
def hello():
    '''
    just say hello
    '''
    click.echo("hello Aure")

@app.cli.command()
def initdb():
    '''
    initilize the database
    '''
    db.create_all()
    click.echo("Database Created ! ")

@app.cli.command()
def create():
    '''
    create the database
    :return:
    '''
    note1 = Note(body="body1")
    note2 = Note(body="body2")
    db.session.add(note1)
    db.session.add(note2)
    db.commit()

if __name__ == '__main__':
    app.run(debug=True)
