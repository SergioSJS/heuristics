import numpy as np
'''
imprime a solucao
'''
def imprime_rota(s):
    var = ''
    for j in range(len(s)):
        if s[j] == -1:
            break
        var += "{} -> ".format(s[j])
    var += "{} \n".format(s[0])
    print(var)
'''
calcula a funcao objetivo
'''
def calcula_fo(s, distancia):
    dist_percorrida = 0
    for j in range(len(s)-1):
        dist_percorrida += distancia[s[j]][s[j+1]]
    dist_percorrida += distancia[s[len(s)-1]][s[0]]
    return dist_percorrida

def insere_meio_vetor(vetor, valor, pos, qde):
    i = qde
    while (i > 0) and (i != pos):
        vetor[i] = vetor[i-1]
        i-=1
    vetor[i] = valor


