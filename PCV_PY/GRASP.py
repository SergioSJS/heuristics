from Construcao import constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo
from Descida import descida_primeiro_melhora

def GRASP(s, d, alpha, GRASP_max):
    iter = 0
    fo_star = float('inf')

    while iter < GRASP_max:
        iter += 1
        constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo(s, d, alpha, 1)

        fo = descida_primeiro_melhora(s, d)
        if fo < fo_star:
            fo_star = fo
            s_star = s.copy()

            print("\Iteracao GRASP = {:3d} \t  fo_star = {:10.3f}".format(iter,fo_star))

    s = s_star.copy()

    return fo_star, s