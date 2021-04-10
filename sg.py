#!/usr/bin/python3
from sqlalchemy import create_engine,Column,Boolean,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import random
def generfield():
        mapa=list(range(1,17))*2
        random.shuffle(mapa)
       
        feld=[]
        fel=[]
        for i in range(32):
            fel.append(mapa[i])
            if  i%8==7:
                feld.append(fel)
                fel=[]
        
        return feld

engine=create_engine('sqlite:///sg.db',connect_args={"check_same_thread": False})
Base = declarative_base()
class Game(Base):
    __tablename__='games'
    id=Column(Integer,primary_key=True)
    cookie=Column(Integer)
    begin=Column(Boolean)
    clck=Column(Boolean)
    lastclicked=Column(Integer)
    field=Column(String)
    th=Column(Integer)
    go=Column(Boolean)
    otoc=Column(Boolean)
    clicky=Column(Integer)
    clickx=Column(Integer)
    bcy=Column(Integer)
    bcx=Column(Integer)
    def __repr__(self):
        return '<id={} cookie={}>'.format(self.id,self.cookie)
Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()



    
def games():
    return list(session.query(Game))
def get(cookie):
    try:
        return session.query(Game).filter(Game.cookie==cookie)[0]
    except IndexError:
        return None
