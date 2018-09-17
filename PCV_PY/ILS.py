import numpy as np

def perturbacao(s, nivel):
    '''
    Reliza perturbação no vetor s uma quantidade de vezes igual a 1 + o nível

    s - vetor
    nivel - nível da perturbacao
    '''
    nTrocas = 0
    n = len(s)

    while nTrocas <= nivel:
        nTrocas += 1
        # Escolhe um vizinho qualquer
        j = np.random.randint(n)
        i = np.random.randint(n)
        while(i == j):
            i = np.random.randint(n)

        # Faz o movimento
        aux = s[i]
        s[i] = s[j]
        s[j] = aux

def ILS(s, d, vezesNivel, ILSmax, buscaLocal, *args):
    '''
    Baseado em: 
    "An ILS-based algorithm to solve a large-scale real heterogeneous fleet VRP with multi-trips and docking constraints"
    http://200.239.128.16/bitstream/123456789/7012/1/ARTIGO_ILSAlgorirhSolve.pdf

    Algoritmo Smart ILS onde temos o parâmetro 'vezesNivel' que determina a quantidade de vezes que um mesmo nível irá repetir
    antes de aumentar.

    s - Vetor solução
    d - Matriz de distâncias
    vezesNivel - número de vezes que irá repetir um nível
    ILSmax - Quantidade de iterações do ILS
    buscaLocal - algoritmo de busca local
    args - demais argumentos

    return - fo final, vetor solução encontrado
    '''
    s_temp = s.copy()
    # Realiza busca local
    fo = buscaLocal(s_temp, d, *args)

    iter = MelhorIter = 0
    nivel = 1
    while iter - MelhorIter < ILSmax:
        iter += 1
        s_temp = s.copy()
        vezes = 0
        while vezes < vezesNivel:
            nTrocasMax = nivel + 1    
            s_temp = s.copy()
            fo_temp = fo

            # Realiza uma perturbação
            perturbacao(s_temp, nTrocasMax)
            # Realiza busca local
            fo_temp = buscaLocal(s_temp, d, *args)
            # Se encontrou solução melhor reseta as variáveis
            if fo_temp < fo:
                fo = fo_temp
                s = s_temp.copy()
                vezes = 0
                nivel = 1
                MelhorIter = iter
                print('fo = {:12.8f}'.format(fo))
            vezes += 1
        print("Aumentando o nivel perturbação para {} \n".format(nivel))
        nivel += 1
    return fo, s
