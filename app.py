import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from api.requests_api import RequestsApi
from Models.Vote import Vote
import random 
aa
app=Flask(__name__)
app.secret_key="655rf677y8989y"

def session_validate():
    if 'login' in session:
        return True
    else:
        return False

@app.route('/')
def index():
    if session_validate()==False:
        return redirect(url_for('login'))

    res=RequestsApi.get_all_api()
    return render_template('index.html', votes=res)

@app.route('/new')
def new():
    if session_validate()==False:
        return redirect(url_for('login'))
    return render_template('create.html')

@app.route('/save', methods=['POST'])
def save():
    if session_validate()==False:
        return redirect(url_for('login'))
    if request.method=='POST':
        try:
             imglist=['di5','1cl','37a','cli','155']
             img=random.choice(imglist)
             value_input=request.form['value_input']
             vote=Vote(value=int(value_input), image_id=img)
             res=RequestsApi.save_api(vote)
             flash('Vote Save')
             return redirect(url_for('index'))
        except:
            flash("Not Save") 

@app.route('/view/<id>')
def view(id):
    if session_validate()==False:
        return redirect(url_for('login'))
    res=RequestsApi.get_one_api(id)
    print(res)
    return render_template('views.html', vote=res)

@app.route('/delete/<id>')
def delete(id):
    if session_validate()==False:
        return redirect(url_for('login'))
    res=RequestsApi.delete_api(id)
    flash('Deleted Vote')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST','GET'])
def login():
    if session_validate()==True:
        return redirect(url_for('index'))
    if request.method=='POST':
        try:
            username=request.form['username']
            password=request.form['password']
            if(username == 'jonatan' and password=='123456'):
                session['login']=True
                session['username']=username
                return redirect(url_for('index'))
            else:
                flash('user not found')
        except:
            flash ("Db Not Conexion")
    return render_template('login.html')

@app.route('/logout')
def logout():
    if session_validate()==False:
        return redirect(url_for('login'))
    session.pop('login',None)
    session.pop('username',None)

    return redirect(url_for('login'))
        
        

if __name__=='__main__':
    app.run(port=8081, debug=True)
