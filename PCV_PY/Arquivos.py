import numpy as np
import math

'''
le um arquivo no formato "numero_cidades melhor_fo_literatura"
'''
def obter_parametros_pcv(nomearq):
    arquivo = np.loadtxt(nomearq)

    num_cidades = int(arquivo[0])
    melhor_fo_lit = float(arquivo[1])

    return num_cidades, melhor_fo_lit


'''
le um arquivo no formato num_cid coord_x coord_y e calcula as distancias d_ij
'''
def le_arq_matriz(nomearq):
    arquivo = np.loadtxt(nomearq)

    distancia = np.empty([len(arquivo), len(arquivo)], dtype=float) # matriz de distancias

    for i in range(len(arquivo)):
        distancia[i][i] = 0.0        
        for j in range(len(arquivo)):
            distancia[i][j] = math.sqrt(pow(arquivo[i][1]-arquivo[j][1],2)+pow(arquivo[i][2]-arquivo[j][2],2))
            distancia[j][i] = distancia[i][j]

    return distancia