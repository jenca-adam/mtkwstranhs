#!/usr/bin/python3
import socket
import time
from flask import Flask, redirect, render_template, abort, request,url_for,make_response 
import os
import json
import random
import erathosten
from json.decoder import JSONDecodeError
from hashlib import sha256
import pickle
import sg
from uu import generfield

games={}
app=Flask(__name__)
rekord=0

def flip(lst,x,y):
    number=lst[x][y]
    if number<=16:
        lst[x][y]+=16
    else:
        lst[x][y]-=16
    return lst
def _random_cookie():
    return str(random.randrange(1829823,289289282)).encode('utf-8')

def get_cookie(function):
    def decorate(*args,**kwargs):
        i=int(request.cookies.get('id'))
        if not sg.get(i):
            g=sg.Game(cookie=i,begin=False,clck=False,lastclicked=-1,field=json.dumps(generfield()),th=0,go=False,otoc=False,clicky=-1,clickx=-1,bcy=-1,bcx=-1)
            sg.session.add(g)
            sg.session.commit()
        a=function(sg.get(i),*args,**kwargs)
         
        sg.session.commit()
        return a
    decorate.__name__=function.__name__
    return decorate
@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pexeso/begin/')
@get_cookie
def pex_bgn(game):
    return render_template('pex.html',field=json.loads(game.field),begin=game.begin,lid=0,clck=game.clck,lastclicked=game.lastclicked,th=game.th,go=game.go,hi=rekord,otoc=game.otoc,clcky=game.clicky,clckx=game.clickx,bcy=game.bcy,bcx=game.bcx)


@app.route('/pexeso/click/<int:y>/<int:x>')
@get_cookie
def pex_clck(game,y,x):
        print(game.clck) 
        game.begin=False
        game.th+=1
        
        clickedbool=game.clck
        
        if(y,x)==(game.clicky,game.clickx) and game.clck:
            return render_template('pex.html',field=json.loads(game.field),begin=game.begin,lid=0,clck=game.clck,lastclicked=game.lastclicked,th=game.th,go=game.go,hi=rekord,otoc=game.otoc,clcky=game.clicky,clckx=game.clickx,bcy=game.bcy,bcx=game.bcx)
                    
        
        game.lastclicked=json.loads(game.field)[y][x]
        game.field=json.dumps(flip(json.loads(game.field),y,x))
        game.clck=not game.clck
        if not game.clck:
            game.bcy=y
            game.bcx=x
            if json.loads(game.field)[y][x]==json.loads(game.field)[game.clicky][game.clickx]:
                f=json.loads(game.field)
                f[y][x]=f[game.clicky][game.clickx]=0
                game.field=json.dumps(f)
            else:
                game.otoc=True
                print('otoc ',game.otoc)
        else:
            print(game.clck)
            game.clicky,game.clickx=y,x
        game.go=True
        for y in range(4):
            for x in range(8):
                if json.loads(game.field)[y][x]>0:
                    game.go=False
                    break
            if not game.go:break
        
        resp=make_response(render_template('pex.html',field=json.loads(game.field),begin=game.begin,lid=0,clck=game.clck,lastclicked=game.lastclicked,th=game.th,go=game.go,hi=rekord,otoc=game.otoc,clcky=game.clicky,clckx=game.clickx,bcy=game.bcy,bcx=game.bcx))
        if game.go:
            resp.set_cookie('id',_random_cookie())
        return resp


@app.route('/pexeso/cancel/<int:y>/<int:x>/<int:by>/<int:bx>')
@get_cookie
def pex_cncl(game,y,x,by,bx):
    game.otoc=False
    game.field=json.dumps(flip(json.loads(game.field),y,x))
    game.field=json.dumps(flip(json.loads(game.field),by,bx))
    return render_template('pex.html',field=json.loads(game.field),begin=game.begin,lid=0,clck=game.clck,lastclicked=game.lastclicked,th=game.th,go=game.go,hi=rekord,otoc=game.otoc,clcky=game.clicky,clckx=game.clickx,bcy=game.bcy,bcx=game.bcx)
@app.route('/pexeso/')
def pxsindx():
    resp=make_response(redirect('/pexeso/begin'))
    return resp
@app.route('/pics/<string:picname>')
def pic(picname):
   return open('pics/'+picname,'rb').read()
    
@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))
if __name__=='__main__':

    app.run(debug=True,port=5000)        

