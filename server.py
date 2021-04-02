import socket
import time
from flask import Flask, redirect, render_template, abort, request,url_for 
import os
import json
import random
import erathosten
from json.decoder import JSONDecodeError
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

@app.route('/nethack/',methods=['GET','POST'])
def nethack():
    if request.method=='POST':
        f=request.form
        u=f['name']
        s.sendto(u.encode('utf-8'),('127.0.0.1',1062))
        b,add=s.recvfrom(1024)
        p=ord(b.decode('utf-8'))
        time.sleep(0.5)
        return redirect('http://localhost:{}'.format(p))
    return render_template('sind.html')
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
def generfield():
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

@app.route('/pexeso/<path:clicked>')
def pex(clicked):
    global field,clickx,clicky,clickedbool,lastclicked,pocet,gover,rekord,otoc,bcly,bclx
    print(clicked)
    begin=False
    lid=False
    if clicked=="begin/":
        lastclicked=0
        pocet=0
        bcly=-1
        bclx=-1
        field=generfield()
        clickx=-1
        clicky=-1
        clickedbool=False
        print(field)
        begin=True
        gover=False
        otoc=False
    elif clicked.startswith('click/'):
        if 'field' not in globals():
            abort(400)
        pocet+=1
        c=clicked.split('/')
        if len(c)!=3:
            abort(400)
        m=c[1:]
        try:
            m=[int(i) for i in m]
        except ValueError:
            abort(400)
        print (clickedbool)
        if( m[0],m[1])==(clicky,clickx) and clickedbool:
            return render_template('pex.html',field=field,begin=begin,lid=lid,clck=clickedbool,lastclicked=lastclicked,th=pocet,go=gover,hi=rekord,otoc=otoc,clcky=clicky,clckx=clickx,bcy=bcly,bcx=bcxy)
        
        field[m[0]][m[1]].flip()
        lastclicked=field[m[0]][m[1]]
        
        if clickedbool:
            bcly=m[0]
            bclx=m[1]
            clickedbool=False
            if field[m[0]][m[1]]==field[clicky][clickx]:
                field[clicky][clickx]=field[m[0]][m[1]]=Obrazok(0)
            else:otoc=True
        else:
            clickedbool=True
            clicky,clickx=m
    elif clicked.startswith('cancel/'):
        otoc=False
        c=clicked.split('/')
        if len(c)!=5:
            abort(400)
        m=c[1:]
        try:
            m=[int(i) for i in m]
        except ValueError:
            abort(400)
        field[m[0]][m[1]].flip()
        field[m[2]][m[3]].flip()

    
    else:
        abort(400)
    gover=True
    for i in field:
        for a in i:
            if a.number!=0:
                gover=False
                print(gover)
                break
        if not gover:
            break
    if gover:
        if pocet>rekord:
            rekord=pocet

    return render_template('pex.html',field=field,begin=begin,lid=lid,clck=clickedbool,lastclicked=lastclicked,th=pocet,go=gover,hi=rekord,otoc=otoc,clcky=clicky,clckx=clickx,bcy=bcly,bcx=bclx)
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

try:
    app.run(debug=True,port=5000)        
except:
    os.system('killall python')
    raise SystemError('ssss')
