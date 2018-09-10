import numpy as np
import time

from Util import imprime_rota, calcula_fo
from Descida import calcula_delta

def SimulatedAnnealing(s, d, alpha, SAmax, temp_inicial, temp_final):  
    s_star = s.copy()
    f_star = fo = calcula_fo(s_star,d)
    temp = temp_inicial

    file_sa = open("SA.txt", 'w')  
    inicio_CPU = fim_CPU = time.clock()
    
    n = len(s)
    file_sa.write('{:4.2f}\t  {:4d}\t  {:7.2f}\n'.format((fim_CPU - inicio_CPU), 0, f_star))
    print("f_star = {:8.2f} \t Temperatura = {:8.2f} \n".format(f_star, temp))

    while temp > temp_final:
        iter = 0
        while iter < SAmax:
            iter += 1
            # Escolhe um vizinho qualquer
            j = np.random.randint(n)
            i = np.random.randint(n)
            while(i == j):
                i = np.random.randint(n)

            # Calcula o custo das arestas envolvidas ANTES do movimento
            delta1 = calcula_delta(s,d,i,j)

            # Faz o movimento
            aux = s[i]
            s[i] = s[j]
            s[j] = aux

            # Calcula o custo das arestas envolvidas DEPOIS do movimento
            delta2 = calcula_delta(s,d,i,j)

            fo_viz = fo - delta1 + delta2
            # Calcula a varia��o de energia
            delta = fo_viz - fo
            if delta < 0:
                fo = fo_viz
                if fo < f_star:
                    f_star = fo
                    s_star = s.copy()
                    fim_CPU = time.clock()
                    file_sa.write('{:4.2f}\t  {:4d}\t  {:7.2f}\n'.format((fim_CPU - inicio_CPU), 0, f_star))
                    print('f_star = {:8.2f} \t Temperatura = {:8.2f} \n'.format(f_star, temp))
            else:
                x= np.random.random()
                if x < np.exp(-delta/temp):
                    fo = fo_viz
                else:
                    ''' Desfaz o movimento caso o vizinho nao seja de melhora
                    ou não passe no teste de aceitação '''
                    aux = s[i]
                    s[i] = s[j]
                    s[j] = aux
        temp = temp * alpha
    
    # temperatura de congelamento do sistema
    s = s_star.copy()
    fim_CPU = time.clock()
    file_sa.write('{:4.2f}\t  {:4d}\t  {:7.2f}\n'.format((fim_CPU - inicio_CPU), 0, f_star))
    file_sa.close()
    return f_star

def calcula_temperatura_inicial(s, d, beta, gamma, SAmax):
    temperatura = 10
    continua = True
    n = len(s)
    while continua:
        aceitos = 0
        iterT = 0
        while iterT < SAmax:
            iterT += 1

            # Escolhe um vizinho qualquer
            j = np.random.randint(n)
            i = np.random.randint(n)
            while(i == j):
                i = np.random.randint(n)

            delta1 = calcula_delta(s, d, i, j)
            # Faz o movimento
            aux = s[j]
            s[j] = s[i]
            s[i] = aux
            delta2 = calcula_delta(s, d, i, j)
            delta = - delta1 + delta2
            if delta < 0:
                aceitos += 1
            else:
                x = np.random.random()
                if (x < np.exp(-delta/temperatura)):
                    aceitos += 1

            # Desfaz o movimento
            aux = s[j]
            s[j] = s[i]
            s[i] = aux
        if aceitos < gamma * SAmax:
            temperatura = beta * temperatura
        else:
            continua = False

    return temperatura