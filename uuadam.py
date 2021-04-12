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
