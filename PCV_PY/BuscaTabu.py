import numpy as np
import time
from Descida import calcula_delta
from Util import imprime_rota, calcula_fo


def lista_candidatos(s, d, fo, fo_star, lista_tabu, iter, duracao):
    n = len(s)
    fo_melhor_viz = float('inf')
    melhor_i = melhor_j = None
    for i in range(n):
        for j in range(i+1, n):
            # Calcula a variação de distância com a realizacao do movimento
            delta1 = calcula_delta(s,d,i,j)
            # Faz o movimento
            s[j], s[i] = s[i], s[j]
            # Calcula nova variação de distância
            delta2 = calcula_delta(s,d,i,j)

            # Calcular a nova distancia
            fo_viz = fo - delta1 + delta2

            if fo_viz < fo_star:
                if fo_viz < fo_melhor_viz:
                    melhor_i = i
                    melhor_j = j
                    fo_melhor_viz = fo_viz
            else:
                na_lista = esta_lista_tabu(lista_tabu, (i, j), iter, duracao)
                if not na_lista:
                    if fo_viz < fo_melhor_viz:
                        melhor_i = i
                        melhor_j = j
                        fo_melhor_viz = fo_viz

            # Desfaz o movimento
            s[j], s[i] = s[i], s[j]

    return fo_melhor_viz, melhor_i, melhor_j
            
''' Verifica se posicao esta na lista tabu'''
def esta_lista_tabu(lista, values, iter, duracao):
    temp = lista[values[0]][values[1]]
    if temp >= iter:
        return True
    else:
        return False

def BuscaTabu(s, d, duracao, bt_max):
    n = len(s)
    file_bt = open("BTsaida.txt", 'w')
    file_bt_melhor = open("BTsaidaMelhorfo.txt", 'w')
    fo_star = fo = calcula_fo(s, d)
    lista_tabu = np.zeros((n,n))

    inicio_CPU = fim_CPU = time.clock()

    print("Iniciando a Busca Tabu com fo = {:8.2f}".format(fo))


    iter = 0 # numero corrente de iteracoes da Busca Tabu
    melhor_iter = 0 # iteracao em que ocorreu a melhor solucao

    s_star = s.copy()

    file_bt.write('{:4.2f}\t  {:7.2f}\n  {:4d}\t'.format((fim_CPU - inicio_CPU), fo, iter))
    file_bt_melhor.write('{:4.2f}\t  {:7.2f}\n  {:4d}\t'.format((fim_CPU - inicio_CPU), fo_star, iter))

    while iter - melhor_iter < bt_max:
        iter += 1

        fo_viz, melhor_j, melhor_i = lista_candidatos(s, d, fo, fo_star, lista_tabu, iter, duracao)

        lista_tabu[melhor_j][melhor_i] = iter+duracao

        # Faz o movimento
        s[melhor_j], s[melhor_i] = s[melhor_i], s[melhor_j]
        fo = fo_viz

        fim_CPU = time.clock()
        file_bt.write('{:4.2f}\t  {:7.2f}\n  {:4d}\t'.format((fim_CPU - inicio_CPU), fo, iter))
        if fo < fo_star:
            melhor_iter = iter
            s_star = s.copy()
            fo_star = fo
            print("fo_star = {:8.2f} \n".format(fo_star))
        file_bt.write('{:4.2f}\t  {:7.2f}\n  {:4d}\t'.format((fim_CPU - inicio_CPU), fo_star, iter))

    fim_CPU = time.clock()
    file_bt.write('{:4.2f}\t  {:7.2f}\n  {:4d}\t'.format((fim_CPU - inicio_CPU), fo, iter))
    file_bt.write('{:4.2f}\t  {:7.2f}\n  {:4d}\t'.format((fim_CPU - inicio_CPU), fo_star, iter))

    print("********** Melhor Solucao Obtida ***************")
    print("Saindo da Busca Tabu com fo_star = {:8.2f}".format(fo_star))
    print("Numero de iteracoes realizadas = {:d} ".format(iter))
    print("********************************************")

    s = s_star.copy()
    fo = fo_star
    return fo, s






