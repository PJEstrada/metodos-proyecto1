# -*- coding: utf-8 -*-
import random

notas = []

for i in range(0,35):
    notas.append(random.randint(0, 101))
w,x,y,z = [],[],[],[]
for nota in notas:
    if 0 <= nota and nota <= 30:
        w.append(nota)
    elif 30 < nota and nota <= 60:
        x.append(nota)
    elif 60 < nota and nota <= 85:
        y.append(nota)
    elif 85 < nota and x <= 100:
        z.append(nota)

print "w-->"+str(w)
print "x-->"+str(x)
print "y-->"+str(y)
print "z-->"+str(z)
print "tamaño w-->"+str(len(w))
print "tamaño x-->"+str(len(x))
print "tamaño y-->"+str(len(y))
print "tamaño z-->"+str(len(z))