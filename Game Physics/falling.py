from time import time 
from math import floor 


y0 = 0.1
v0 = 7
a = -1.9 

fixed = time()
def t():
    return time() - fixed 

def y(): 
    return y0 + v0*t() + 0.5*a*(t() ** 2)

y_f = y()                    # initial displacement
last_integer = floor(y_f)    # store the last integer time

fout = open('out.txt', 'w')
while y_f > 0:
    if not last_integer == floor(y()): 
        last_integer = floor(y())
        print(last_integer)
        fout.write(f'Time: {t():.2f} >>> y_f: {y_f:.2f}\n')

    y_f = y()
fout.close()