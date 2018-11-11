from Util import imprime_rota, calcula_fo
from Construcao import constroi_solucao_gulosa_vizinho_mais_proximo, \
            constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo, \
            constroi_solucao_gulosa_insercao_mais_barata, \
            constroi_solucao
from Descida import descida, \
            descida_randomica, \
            descida_primeiro_melhora

import numpy as np
# vnd 
def AG(
    s, 
    d, 
    nind, 
    max_desvio, 
    prob_crossover, 
    prob_mutacao,
    tipo_operador):
    
    n = len(s)
    fo_star = float('inf')

    if (nind % 2 != 0):
        print("Numero de individuos deve ser par!")
        print("Vou aumentar o numero de individuos ...")
        nind += 1

    nind = nind * 2

    pop = np.zeros((nind, n))
    fo_pop = np.zeros(nind)    

    pop_sobrev = np.zeros((nind/2, n))
    fo_pop_sobrev = np.zeros((nind/2))

    # Geracao da populacao inicial
    for j in range(nind/2)
        # GRASP(n, pop[j], d, 0.10, 10, 1);
        constroi_solucao(s)
        np.random.shuffle(s)
        
        # constroi_solucao_aleatoria(n, pop[j], d)
        # constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo(n, pop[j], d, 0.05);
        # constroi_solucao_parcialmente_gulosa_insercao_mais_barata(n, pop[j], d, 0.05);
        fo_pop[j] = calcula_fo(pop[j], d)
        
        if (fo_pop[j] < fo_star):
            fo_star = fo_pop[j]
            s_star = pop[j].copy()                 

    print("Melhor solucao encontrada na construcao: {:%f}".format(fo_star));

    int ngeracoes = 0;
    float desvio = INT_MAX;
    while (desvio > max_desvio){
      ngeracoes++;
      /* Aplicar crossover */
      int quant_filhos = 0;
      while (quant_filhos < nind/2){
          /* Selecao aleatoria de pais */
          int jpai1, jpai2;
          do{
            jpai1 = rand()%(nind/2);
            jpai2 = rand()%(nind/2);
          }while (jpai1 == jpai2);
          if (randomico(0,1) < prob_crossover){
                /*
                Refinando os pais antes de eles procriarem:
                descida_primeiro_melhora(n,pop[jpai1],d);
                descida_primeiro_melhora(n,pop[jpai2],d);
                */

             if (tipo_operador == 1)
               crossover_OX(pop[jpai1], pop[jpai2], pop[quant_filhos+nind/2], pop[quant_filhos+nind/2+1], n);
             if (tipo_operador == 2)
               crossover_ERX(pop[jpai1], pop[jpai2], pop[quant_filhos+nind/2], pop[quant_filhos+nind/2+1], n);
             quant_filhos+=2;
          }
      }
      /* Aplicar mutacao */
      for (int j = 0; j < nind; j++)
        if (randomico(0,1) < prob_mutacao)
           mutacao(pop[j], n);

      /* Avaliar a populacao inteira (pais e filhos) */
      for (int j = 0; j < nind; j++){
        fo_pop[j] = calcula_fo(n, pop[j], d);
        if (fo_pop[j] < fo_star){
           fo_star = fo_pop[j];
           atualiza_vetor(s_star, pop[j], n);
           printf("Geracao = %4d   fo star = %10.3f\n", ngeracoes, fo_star);
        }
      }

      /* Definir a populacao sobrevivente */
      /* fo de todos os individuos da populacao, isto é, pais e filhos */
      for (int j = 0; j < nind/2; j++){
        /* escolha dos individuos sobreviventes pelo mecanismo da roleta */
        int individuo_escolhido = roleta(nind, fo_pop);
        /* escolha dos individuos sobreviventes pelo mecanismo da roleta
           colocando aptidao nula para aqueles que estiverem acima de uma dada
           faixa, no caso, duas vezes de desvio padrao acima da media */
        //int individuo_escolhido = roleta_scaling(nind, fo_pop);
        for (int i = 0; i < n; i++) pop_sobrev[j][i] = pop[individuo_escolhido][i];
        fo_pop_sobrev[j] = fo_pop[individuo_escolhido];

      }
      /* Zerar a populacao e seus dados */
      inicializa_vetor_float(fo_pop,nind);
      for (int j = 0; j < nind; j++) inicializa_vetor(pop[j],n);
      /* Primeira metade da populacao <-- populacao sobrevivente */
      for (int j = 0; j < nind/2; j++){
        for (int i = 0; i < n; i++) pop[j][i] = pop_sobrev[j][i];
        fo_pop[j] = fo_pop_sobrev[j];
      }


      /* Zerar a matriz e os vetores que armazenam os dados da populacao sobrevivente */
      inicializa_vetor_float(fo_pop_sobrev,nind/2);
      for (int j = 0; j < nind/2; j++) inicializa_vetor(pop_sobrev[j],n);

      /* Calcular o desvio padrão das fos da população */
      desvio = calcula_desvio_padrao(fo_pop,nind/2);
    }

    atualiza_vetor(s, s_star, n);
    fo = fo_star;
    printf("\nNumero de geracoes avaliadas: %d\n", ngeracoes);

    libera_matriz(pop, nind);
    free(fo_pop);
    libera_matriz(pop_sobrev, nind/2);
    free(fo_pop_sobrev);
    libera_vetor(s_star);

    return fo;