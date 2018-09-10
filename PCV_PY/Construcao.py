import numpy as np
import heapq as hq
from Util import *

'''
Constroi uma solução simples atribuindo índice ao valor
'''
def constroi_solucao(s):
    for j in range(len(s)):
        s[j] = j    

'''
Constroi uma solucao de forma gulosa, no caso,
implementa o Metodo construtivo do vizinho mais proximo
'''
def constroi_solucao_gulosa_vizinho_mais_proximo(s, d):

    # Inicio da Fase de Construcao de uma solucao
    print("Construindo nova solucao ...")

    lista_c = []
    for j in range(1, len(s)):
        lista_c.append([j, 0, 0.0])

    s[0] = 0 # A cidade origem é a cidade 0

    for j in range(1, len(s)):
        dist = float('inf')
        for i, registro in enumerate(lista_c):
            if d[s[j-1]][registro[0]] < dist:
                dist = d[s[j-1]][registro[0]]
                mais_proxima = registro[0]                
                idx_mais_proxima = i
        # Insere a cidade mais proxima após a ultima cidade inserida
        s[j] = mais_proxima
        # Apaga a cidade mais_proxima da lista de nao visitadas
        lista_c.pop(idx_mais_proxima)
   
'''
Constroi uma solucao parcialmente gulosa pelo metodo do vizinho mais proximo
'''
def constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo(s, d, alpha):
     # Inicio da Fase de Construcao de uma solucao
    print("Construindo nova solucao ...")

    lista_c = []
    for j in range(1, len(s)):
        lista_c.append([j, 0, 0.0])

    s[0] = 0 # A cidade origem é a cidade 0
    
    for j in range(1, len(s)):
        # Apaga a lista de candidatos ordenada
        LC_ordenada = []
        for i, registro in enumerate(lista_c):
            nao_visitada = []
            nao_visitada.append(registro[0])
            nao_visitada.append(registro[1])
            nao_visitada.append(d[s[j-1]][nao_visitada[0]])
            # inserir um registro de forma ordenada em uma lista
            hq.heappush(LC_ordenada, (nao_visitada[2], nao_visitada))

        tamanho_LRC = max(1, alpha * len(lista_c))
        posicao_escolhida = np.random.randint(tamanho_LRC)
        registro = LC_ordenada[posicao_escolhida]
        cidade_escolhida = registro[1][0]


        # Insere a cidade escolhida apos a ultima cidade inserida
        s[j] = cidade_escolhida
        # Apaga a cidade mais_proxima da lista de nao visitadas
        for i, l in enumerate(lista_c):
            if l[0] == cidade_escolhida:
                lista_c.pop(i)
                break        
'''
Constroi uma solucao pela inserção mais barata
'''
def constroi_solucao_gulosa_insercao_mais_barata(s, d):
     # Inicio da Fase de Construcao de uma solucao
    print("Construindo nova solucao ...")

    lista_c = []
    for j in range(1, len(s)):
        lista_c.append([j, 0, 0.0])

    s[0] = 0 # A cidade origem é a cidade 0

    # Insere as duas proximas cidades pela heurística do vizinho mais próximo
    for j in range(1,3):
        dist = float('inf')
        for i, registro in enumerate(lista_c):
            if d[s[j-1]][registro[0]] < dist:
                dist = d[s[j-1]][registro[0]]
                mais_proxima = registro[0]                
                idx_mais_proxima = i
        # Insere a cidade mais proxima após a ultima cidade inserida
        s[j] = mais_proxima
        # Apaga a cidade mais_proxima da lista de nao visitadas
        lista_c.pop(idx_mais_proxima)
    '''
    Formada uma subrota inicial com tres cidades, aplicar o metodo da
    insercao mais barata para decidir qual cidade inserir entre cada
    par de cidades i e j. A cidade k escolhida sera aquela que minimizar
    custo(k) = d(i,k) + d(k,j) - d(i,j)
    '''
    for j in range(3, len(s)):
        melhor_sij = float('inf')
        idx_apaga = None
        # Calcula os custos para cada cidade k ser inserida entre as cidades i e j
        for idx, registro in enumerate(lista_c):
            cid_k = registro[0]
            for i in range(0, j):
                cid_i = s[i]
                if i+1 != j:
                    cid_j = s[i+1]
                else:
                    cid_j = 0
                # calcula distância entre as cidades i e j
                sij = d[cid_i][cid_k] + d[cid_k][cid_j] - d[cid_i][cid_j]
                if (sij < melhor_sij):
                    melhor_i = cid_i
                    melhor_k = cid_k
                    melhor_sij = sij
                    idx_apaga = idx
        # procura a posição do vetor a ser inserida a cidade
        for i in range(0, j):
            if s[i] == melhor_i:
                pos = i+1
        
        # Adiciona cada nova cidade k entre as cidades i e j que produzir a inserção mais barata
        #print(pos, melhor_k)
        insere_meio_vetor(s, melhor_k, pos, j)

        # Apaga a cidade mais_proxima da lista de nao visitadas
        if idx_apaga != None:
            lista_c.pop(idx_apaga)