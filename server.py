#!/usr/bin/python3
import socket
import time
from flask import Flask, redirect, render_template, abort, request,url_for 
import os
import json
import random
import erathosten
from json.decoder import JSONDecodeError
from hashlib import sha256
import pickle
class Obrazok:
    def __init__(self,name):
        self.number=name
        self.showed=False
    def __repr__(self):
        return str(self.number)
    def __eq__(self,obj):
        if isinstance(obj,Obrazok) and obj.number == self.number :
            return True
        return False

    def flip(self):
        self.showed= not self.showed

class Game:
    def __init__(self):
        self.field=self.generfield()
        self.begin=True
        self.clck=False
        self.lastclicked=0
        self.th=0
        self.go=False
        self.otoc=False
        self.clicky=-1
        self.clickx=-1
        self.bcy=-1
        self.bcx=-1
    def __getattr__(self,a):
        if a=='game':
            return self
        raise AttributeError
    def generfield(self):
        mapa=list(range(1,17))*2
        mapa=[Obrazok(i) for i in mapa]
        random.shuffle(mapa)
       
        feld=[]
        fel=[]
        for i in range(32):
            fel.append(mapa[i])
            if  i%8==7:
                feld.append(fel)
                fel=[]
        
        return feld

class DictClass:
    def __init__(self,d):
        self.__dict__.update(d)
games={}
os.system('python s.py &')
app=Flask(__name__)
rekord=0
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/primes/')
def eratho():
    return render_template('basic.html')
@app.route('/zisti/',methods=['POST'])
def zisti():
    if request.method=='POST':
        form=request.form
        num=form['cislo']
        try:
            num=int(num)
        except ValueError:
            return render_template('zisti.html',chyba='Toto nie je cislo')
        courobit=form['courobit']
        if courobit=='prve':
            return  render_template('zisti.html',title="Prvých {num} prvočísel".format(num=num), vysledok=sformatuj(erathosten.primes(int(num)),num))
        elif courobit =='vsetky':
            return  render_template('zisti.html',title="Všetky prvočísla < {num}".format(num=num), vysledok=sformatuj(erathosten.primesrange(int(num)),num))
  
        else:
            return  render_template('zisti.html',title="Je čislo {num} prvočíslo?".format(num=num), vysledok=sformatuj(erathosten.isprime(int(num)),num))
def sformatuj(vec,cislo):
    if isinstance(vec,bool):
        if vec:
            return 'Ano, číslo {cislo} je prvočíslo.'.format(cislo=cislo)
        else:
            return 'Nie, číslo {cislo} nie je prvočíslo.'.format(cislo=cislo)
    elif isinstance(vec,list):
        return' '.join([str(i) for i in vec])
    else:
        return 'Niekde je chIba'

try:
    urls=json.load(open('urls.json','r'))
except JSONDecodeError:
    urls={}
@app.route('/urlshorten/')
def applet():
    return render_template('urlshorten.html')

@app.route('/add/' ,methods=['POST'])
def add():
    global urls
    try:
        urls=json.load(open('urls.json','r'))
    except:
        urls={}
    if request.method=='POST':
        f=request.form
        long=f['long']
        alias=f['alias']
        urls[alias]=long
        print(urls)
    json.dump(urls,open('urls.json','w'))
    return redirect('/')
@app.route('/urlshorten/<string:alias>/')
def get(alias):
    urls=json.load(open('urls.json','r'))
    print(alias)
    if alias not in urls:
        abort(404)
    return redirect(urls[alias])
@app.route('/pexeso/<path:clicked>')
def pex(clicked):
    global rekord,game
    games=pickle.load(open('games.pickle','rb'))
    print(clicked)
    begin=False
    lid=False
    try:
        game=DictClass(games[request.remote_addr])
    except KeyError:pass
    if clicked=="begin/":
        games[request.remote_addr]=Game().__dict__
        game=DictClass(games[request.remote_addr])
        pickle.dump(games,open('games.pickle','wb'))
        games=pickle.load(open('games.pickle','rb'))
        print(clicked)
        begin=False
        lid=False
        print(games)


    


    elif clicked.startswith('click/'):
        game=DictClass(games[request.remote_addr])

        print(game.otoc) 
       
        game=DictClass(games[request.remote_addr])
        game.begin=False
        game.th+=1
        
        c=clicked.split('/')
        if len(c)!=3:
            abort(400)
        m=c[1:]
        try:
            m=[int(i) for i in m]
        except ValueError:
            abort(400)
        clickedbool=game.clck
        print (clickedbool)
        if( m[0],m[1])==(game.clicky,game.clickx) and game.clck:
            return render_template('pex.html',field=game.field,begin=game.begin,lid=0,clck=game.clck,lastclicked=game.lastclicked,th=game.th,go=game.go,hi=rekord,otoc=game.otoc,clcky=game.clicky,clckx=game.clickx,bcy=game.bcy,bcx=game.bcx)
                    
        game.field[m[0]][m[1]].flip()
        game.lastclicked=game.field[m[0]][m[1]]
        
        if game.clck:
            game.bcy=m[0]
            game.bcx=m[1]
            game.clck=False
            if game.field[m[0]][m[1]]==game.field[game.clicky][game.clickx]:
                game.field[game.clicky][game.clickx]=game.field[m[0]][m[1]]=Obrazok(0)
            else:
                game.otoc=True
                print(game.otoc)
        else:
            game.clck=True
            game.clicky,game.clickx=m
    elif clicked.startswith('cancel/'):
        game=DictClass(games[request.remote_addr])

        game.otoc=False
        c=clicked.split('/')
        if len(c)!=5:
            abort(400)
        m=c[1:]
        try:
            m=[int(i) for i in m]
        except ValueError:
            abort(400)
        game.field[m[0]][m[1]].flip()
        game.field[m[2]][m[3]].flip()

    
    else:
        abort(400)
    game.go=True
    for i in game.field:
        for a in i:
            if a.number!=0:
                game.go=False
                
                break
        if not game.go:
            break
    if game.go:
        if game.th<rekord:
            rekord=game.th
    games[request.remote_addr].update(game.__dict__)
    pickle.dump(games,open('games.pickle','wb'))
    game=DictClass(games[request.remote_addr])

    return render_template('pex.html',field=game.field,begin=game.begin,lid=0,clck=game.clck,lastclicked=game.lastclicked,th=game.th,go=game.go,hi=rekord,otoc=game.otoc,clcky=game.clicky,clckx=game.clickx,bcy=game.bcy,bcx=game.bcx)
@app.route('/pexeso/')
def pxsindx():
    return redirect('/pexeso/begin/')
@app.route('/pics/<string:picname>')
def pic(picname):
    try:
        return open('pics/'+picname,'rb').read()
    except: abort(404)
@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))
if __name__=='__main__':
    try:
        app.run(debug=True,port=5000)        
    except:
        os.system('killall python')
        raise SystemError('ssss')
