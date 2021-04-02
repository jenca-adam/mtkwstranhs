#!/usr/bin/python
import sys,cmd,math
def primes(num):
    primes=[]
    index=2
    end=False
    primecount=0
    while True:
            i=True
            for prime in primes[:int(math.sqrt(index))+1]:
                if index%prime == 0:
                    i=False
                    break
            if i:
                primes.append(index)
                primecount+=1
                if primecount==num:
                    break
            index+=1
    return primes
def primesrange(num):
    primes=[]
    index=2
    for prime in range(num-1):
            i=True
            for prime in primes[:int(math.sqrt(index))+1]:
                if index%prime == 0:
                    i=False
                    break
            if i:
                primes.append(index)
            index+=1
    return primes
def isprime(num):
    return num in primesrange(num)
class CMDLine(cmd.Cmd):
    def do_mensie(self,line):
        print(*primesrange(int(line)))
    def do_vsetky(self,line):
        print(*primes(int(line)))
    def do_spytaj(self,line):
        print(isprime(int(line)))
    def help_mensie(self):
        print('mensie [n]. vrati vsetky prvocisla p<n')
    def help_vsetky(self):
        print('vsetky [n]. vrati prvych n prvocisel')
    def help_spytaj(self):
        print('spytaj [n]. zistuje, ci je n prvocislom, ak je povie True, inak False')
    def do_EOF(self,line):
        exit()
if __name__=='__main__':
    CMDLine().cmdloop()
