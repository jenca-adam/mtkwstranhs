import random
def generfield():
    mapa=list(range(1,13))*2
    random.shuffle(mapa)
   
    feld=[]
    fel=[]
    for i in range(24):
        fel.append(mapa[i])
        if  i%6==5:
            feld.append(fel)
            fel=[]
    
    return feld
def genmobfield():
    mapa=list(range(1,13))*2
    random.shuffle(mapa)
   
    feld=[]
    fel=[]
    for i in range(24):
        fel.append(mapa[i])
        if  i%4==3:
            feld.append(fel)
            fel=[]
    
    return feld

