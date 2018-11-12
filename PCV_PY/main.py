'''
Tecnicas Heuristicas para resolucao do Problema do Caixeiro Viajante
Autor: Sérgio José de Sousa
Email: sergio7sjs@gmail.com
Data: 28/08/2018

Projeto em C convertido para Python
    Autor: Marcone Jamilson Freitas Souza
    Local: Departamento de Computacao - Universidade Federal de Ouro Preto
    Homepage: www.decom.ufop.br/prof/marcone
    Data: 21-05-2007
'''
import sys
import numpy as np
import time

from Arquivos import *
import Menus
from Util import imprime_rota, calcula_fo
from Construcao import constroi_solucao_gulosa_vizinho_mais_proximo, \
            constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo, \
            constroi_solucao_gulosa_insercao_mais_barata, \
            constroi_solucao
from Descida import descida, \
            descida_randomica, \
            descida_primeiro_melhora

from BuscaTabu import BuscaTabu

from ILS import ILS

from SimulatedAnnealing import calcula_temperatura_inicial, \
            SimulatedAnnealing

from GRASP import GRASP

from AG import AG

def main():
    fo = 0.0 # funcao objetivo corrente
    # clock_t 
    inicio_CPU = 0.0 # clock no inicio da aplicacao do metodo
    fim_CPU  = 0.0 # clock no final da aplicacao do metodo

    n, melhor_fo_lit = obter_parametros_pcv("C50INFO.TXT")#obter_parametros_pcv("C50INFO.TXT") # n = numero de cidades; melhor_fo_lit = melhor fo da literatura
    s = np.empty([n], dtype=int) # vetor solucao
    d = le_arq_matriz("C50.TXT") # matriz de distancias
    #d = le_arq_matriz("A280.TXT") # matriz de distancias
    
    while True:
        escolha = Menus.menu_principal()
        # Geracao de uma solucao inicial
        if escolha == 1:
            soluc_ini = Menus.menu_solucao_inicial()
            # Geracao gulosa de uma solucao inicial via metodo do vizinho mais proximo
            if soluc_ini == 1:
                constroi_solucao_gulosa_vizinho_mais_proximo(s,d)
                fo = calcula_fo(s, d)
                print("Solucao construida de forma gulosa (Vizinho Mais Proximo):")
                imprime_rota(s)
                print("Funcao objetivo = {}".format(fo))
            # Geracao parcialmente gulosa de uma solucao inicial via metodo do vizinho mais proximo
            elif soluc_ini == 2:
                constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo(s,d,0.05)
                fo = calcula_fo(s, d)
                print("Solucao construida de forma gulosa (Vizinho Mais Proximo):")
                imprime_rota(s)
                print("Funcao objetivo = {}".format(fo))
            # Geracao gulosa de uma solucao inicial via metodo da insercao mais barata
            elif soluc_ini == 3:
                constroi_solucao_gulosa_insercao_mais_barata(s,d)
                fo = calcula_fo(s, d)
                print("Solucao construida de forma gulosa (Insercao Mais Barata):")
                imprime_rota(s)
                print("Funcao objetivo = {}".format(fo))
            # Geracao parcialmente gulosa de uma solucao inicial via insercao mais barata
            elif soluc_ini == 4:
                print("Ainda nao implementado...")
            # Geracao aleatória de uma solucao inicial
            elif soluc_ini == 5:                
                constroi_solucao(s)
                np.random.shuffle(s)
                fo = calcula_fo(s, d)
                print("Solucao construida de forma aleatoria:")
                imprime_rota(s)
                print("Funcao objetivo = {}".format(fo))
        # Descida
        elif escolha == 2:
            inicio_CPU = time.clock()
            fo = descida(s,d)
            fim_CPU = time.clock()
            print("Solucao obtida usando a estrategia Best Improvement do Metodo da Descida:")
            imprime_rota(s)
            print("Funcao objetivo = {}".format(fo))
            print("Tempo de CPU = {} segundos:".format((fim_CPU - inicio_CPU)))
        # Descida Randômica
        elif escolha == 3:
            n = len(s)
            it = 0.7*(n*(n-1)/2)
            it = int(it)
            inicio_CPU = time.clock()
            fo = descida_randomica(s,d, it)
            fim_CPU = time.clock()
            print("Solucao obtida usando a estrategia Best Improvement do Metodo da Descida Randômica:")
            imprime_rota(s)
            print("Funcao objetivo = {}".format(fo))
            print("Tempo de CPU = {} segundos:".format((fim_CPU - inicio_CPU)))
        # Descida com primeiro de melhora
        elif escolha == 4:
            inicio_CPU = time.clock()
            fo = descida_primeiro_melhora(s,d)
            fim_CPU = time.clock()
            print("Solucao obtida usando a estrategia Best Improvement do Metodo da Descida com primeiro de melhora:")
            imprime_rota(s)
            print("Funcao objetivo = {}".format(fo))
            print("Tempo de CPU = {} segundos:".format((fim_CPU - inicio_CPU)))
        # Multi-Start
        elif escolha == 5:
            print("Nao implementado")
            break
        # Simulated Annealing
        elif escolha == 6:
            inicio_CPU = time.clock()

            temp_inicial = calcula_temperatura_inicial(s,d,1.1,0.95,500)            
            fo = SimulatedAnnealing(s,d,0.99,2*n,temp_inicial,0.01)

            fim_CPU = time.clock()
            print("Solucao obtida usando a estrategia Simulated Annealing:")
            imprime_rota(s)
            print("Funcao objetivo = {}".format(fo))
            print("Tempo de CPU = {} segundos:".format((fim_CPU - inicio_CPU)))

        # Busca Tabu
        elif escolha == 7:
            inicio_CPU = time.clock()
            fo, s = BuscaTabu(s, d, 15, 5000)
            fim_CPU = time.clock()

            print("Solucao obtida usando a estrategia Busca Tabu:")
            imprime_rota(s)
            print("Funcao objetivo = {}".format(fo))
            print("Tempo de CPU = {} segundos:".format((fim_CPU - inicio_CPU)))


        # Iterated Local Search
        elif escolha == 8:
            inicio_CPU = time.clock()
 
            buscaLocal = Menus.menu_busca_local()
            if buscaLocal == 1:
                fo, s = ILS(s,d, 15, 30, descida)
            elif buscaLocal == 2:
                it = 0.7*(n*(n-1)/2)
                fo, s = ILS(s,d, 15, 30, descida_randomica, it)
            elif buscaLocal == 3:
                fo, s = ILS(s,d, 15, 30, descida_primeiro_melhora)            
            
            fim_CPU = time.clock()
            print("Solucao obtida usando a estrategia Iterated Local Search:")
            imprime_rota(s)
            print("Funcao objetivo = {}".format(fo))
            print("Tempo de CPU = {} segundos:".format((fim_CPU - inicio_CPU)))
        # GRASP
        elif escolha == 9:
            grasp_op = Menus.menu_GRASP()
            # Geracao Parcialmente gulosa de uma solucao inicial via metodo do vizinho mais proximo
            if grasp_op == 1:
                inicio_CPU = time.clock()
                print("Solucao gerada pelo Metodo GRASP:")
                fo, s = GRASP(s, d, 0.05, 100)
                imprime_rota(s)
                fim_CPU = time.clock()

                print("Funcao objetivo = {}".format(fo))
                print("Tempo de CPU = {} segundos:".format((fim_CPU - inicio_CPU)))
            # Geracao parcialmente gulosa de uma solucao inicial via metodo da insercao mais barata
            elif grasp_op == 2:
                print("Nao implementado")
                break
        # VND
        elif escolha == 10:
            print("Nao implementado")
            break
        # VNS
        elif escolha == 11:
            print("Nao implementado")
            break
        # Algoritmos Geneticos
        elif escolha == 12:
            ag_op = Menus.menu_AG()
            # Algoritmos Geneticos usando operador OX
            if ag_op == 1:
                inicio_CPU = time.clock()
                fo, s = AG(s,d,100,0.03,0.85,0.01,1)
                fim_CPU = time.clock()

                print("Solucao por AG usando operador OX:")
                print("fo = {:10.2f} ".format(fo))
                print("Tempo de execução = {:10.2f} segundos".format(fim_CPU - inicio_CPU))
                imprime_rota(s)
                
            # Algoritmos Geneticos usando operador ERX
            elif ag_op == 2:
                inicio_CPU = time.clock()
                fo, s = AG(s,d,100,0.03,0.85,0.01,2)
                fim_CPU = time.clock()

                print("Solucao por AG usando operador ERX:")
                print("fo = {:10.2f} ".format(fo))
                print("Tempo de execução = {:10.2f} segundos".format(fim_CPU - inicio_CPU))
                imprime_rota(s)        
        # Algoritmos Memeticos
        elif escolha == 13:
            print("Nao implementado")
            break
        # Colonia de Formigas
        elif escolha == 14:
            print("Nao implementado")
            break
        else:
            break

if __name__ == "__main__": 
    main()