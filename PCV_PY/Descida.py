import numpy as np
import time

from Util import imprime_rota, calcula_fo

def calcula_delta(s, d, i, j):
    n = len(s)
    i_antes = i - 1
    i_depois = i + 1
    j_antes = j - 1
    j_depois = j + 1
    if (i == 0):
        i_antes = n-1
    if (i == n-1):
        i_depois = 0
    if (j == 0):
        j_antes = n-1
    if (j == n-1):
        j_depois = 0

    return  d[s[i_antes]][s[i]] + d[s[i]][s[i_depois]] + d[s[j_antes]][s[j]] + d[s[j]][s[j_depois]]
    #delta = d[s[i-1]][s[i]] + d[s[i]][s[i+1]] + d[s[j-1]][s[j]] + d[s[j]][s[j+1]]

def melhor_vizinho(s, d, fo, melhor_i, melhor_j):
    fo_melhor_viz = fo
    
    for i in range(len(s)-1):
        for j in range(len(1+s)):
            # Calcula a variacao de custo com a realizacao do movimento
            delta1 = calcula_delta(s, d, i, j)
            # Faz o movimento
            aux = s[j]
            s[j] = s[i]
            s[i] = aux

            delta2 = calcula_delta(s, d, i, j)

            # Calcular a nova distancia
            fo_viz = fo - delta1 + delta2

            # Armazenar o melhor movimento (melhor troca)
            if fo_viz < fo_melhor_viz:
                melhor_i = i
                melhor_j = j
                fo_melhor_viz = fo_viz
            
            # Desfaz o movimento
            aux = s[j]
            s[j] = s[i]
            s[i] = aux
    # retornar a distancia do melhor vizinho
    return fo_melhor_viz, melhor_i, melhor_j

def descida(s, d):  
    fo = fo_viz = calcula_fo(s, d)

    melhor_i = None
    melhor_j = None

    file_descida = open("Descida.txt", 'w')  
    inicio_CPU = fim_CPU = time.clock()

    file_descida.write('{:4.2f}\t  {:4d}\t  {:7.2f}\n'.format((fim_CPU - inicio_CPU), 0, fo))
    while True:
        melhorou = False
        fo_viz, melhor_i, melhor_j = melhor_vizinho(s, d, fo, melhor_i, melhor_j)
        if fo_viz < fo:
            #print("Rota antes:  Fo antes = {} \n".format(fo))
            #imprime_rota(s)

            aux = s[melhor_j]
            s[melhor_j] = s[melhor_i]
            s[melhor_i] = aux

            fo = fo_viz
            melhorou = True
            fim_CPU = time.clock()
            file_descida.write('{:4.2f}\t  {:4d}\t  {:7.2f}\n'.format((fim_CPU - inicio_CPU), 0, fo))

            #print("Vou trocar {} com {} \n".format(melhor_i,melhor_j))
            #print("Rota depois do movimento: Fo melhor vizinho = {} \n".format(fo_viz))
            #imprime_rota(s)
        if melhorou != True:
            break
    fim_CPU = time.clock()
    file_descida.write('{:4.2f}\t  {:4d}\t  {:7.2f}\n'.format((fim_CPU - inicio_CPU), 0, fo))
    file_descida.close()
    return fo

def descida_randomica(s, d, IterMax):    
    fo = calcula_fo(s,d)
    n = len(s)
    iter = 0
    while iter < IterMax:
        iter += 1
        j = np.random.randint(n)
        i = np.random.randint(n)
        while(i == j):
            i = np.random.randint(n)
        
        delta1 = calcula_delta(s, d, i, j)

        aux = s[i]
        s[i] = s[j]
        s[j] = aux

        delta2 = calcula_delta(s, d, i, j)
        fo_viz = fo - delta1 + delta2

        if fo_viz < fo:
            iter = 0
            fo = fo_viz        
        else:
            aux = s[i]
            s[i] = s[j]
            s[j] = aux
    return fo

def vizinho_primeiro_melhora(s, d, fo, melhor_i, melhor_j):
    fo_melhor_viz = fo
    melhorou = False    
    n = len(s)

    vet = np.arange(n)
    np.random.shuffle(vet)

    for i in range(n-1):
        for j in range(i+1, n):
            # Calcula a variacao de custo com a realizacao do movimento
            delta1 = calcula_delta(s,d,vet[i],vet[j])

            # Faz o movimento
            aux = s[vet[j]]
            s[vet[j]] = s[vet[i]]
            s[vet[i]] = aux

            delta2 = calcula_delta(s,d,vet[i],vet[j])

            # Calcular a nova distancia
            fo_viz = fo - delta1 + delta2

            # Armazenar o melhor movimento (melhor troca)
            if fo_viz < fo_melhor_viz:
                melhor_i = vet[i]
                melhor_j = vet[j]
                
                fo_melhor_viz = fo_viz
                melhorou = True

            # Desfaz o movimento
            aux = s[vet[j]]
            s[vet[j]] = s[vet[i]]
            s[vet[i]] = aux
            if melhorou:
                break
        if melhorou:
            break
    # retornar a distancia do melhor vizinho
    return fo_melhor_viz, melhor_i, melhor_j

def descida_primeiro_melhora(s, d):
    aux = melhor_i = melhor_j = 0
    
    fo = fo_viz = calcula_fo(s, d)
    file_descida = open("DescidaPrimeiroMelhora.txt", 'w')  
    inicio_CPU = fim_CPU = time.clock()

    file_descida.write('{:4.2f}\t  {:4d}\t  {:7.2f}\n'.format((fim_CPU - inicio_CPU), 0, fo))
    while True:
        melhorou = False
        fo_viz, melhor_i, melhor_j = vizinho_primeiro_melhora(s, d, fo, melhor_i, melhor_j)
        if (fo_viz < fo):
            #print("Rota antes:  Fo antes = {}", fo);
            #imprime_rota(s);

            aux = s[melhor_j]
            s[melhor_j] = s[melhor_i]
            s[melhor_i] = aux

            fo = fo_viz
            melhorou = True
            fim_CPU = time.clock()
            file_descida.write('{:4.2f}\t  {:4d}\t  {:7.2f}\n'.format((fim_CPU - inicio_CPU), 0, fo))

            #print("Vou trocar {} com {}".format(melhor_i,melhor_j))
            #print("Rota depois do movimento: Fo melhor vizinho = {}".format(fo_viz))
            #imprime_rota(s)
        if not melhorou:
            break
    fim_CPU = time.clock()
    file_descida.write('{:4.2f}\t  {:4d}\t  {:7.2f}\n'.format((fim_CPU - inicio_CPU), 0, fo))
    file_descida.close()
    
    return fo