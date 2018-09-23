import numpy as np
from Descida import calcula_delta

def lista_candidatos(s, d):
    n = len(s)
    for i in range(n):
        for j in range(i+1, n):
            
