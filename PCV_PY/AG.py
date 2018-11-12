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
def AG(s, d, nind, max_desvio, prob_crossover, prob_mutacao, tipo_operador):

	n = len(s)
	fo_star = float('inf')

	if (nind % 2 != 0):
		print("Numero de individuos deve ser par!")
		print("Vou aumentar o numero de individuos ...")
		nind += 1

	nind = nind * 2

	pop = np.zeros((nind, n), dtype=int)
	fo_pop = np.zeros(nind, dtype=int)    

	pop_sobrev = np.zeros((int(nind/2), n), dtype=int)
	fo_pop_sobrev = np.zeros(int(nind/2), dtype=int)

	# Geracao da populacao inicial
	for j in range(int(nind/2)):
		# GRASP(n, pop[j], d, 0.10, 10, 1);
		constroi_solucao(pop[j])
		np.random.shuffle(pop[j])

		# constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo(pop[j], d, 0.05);
		# constroi_solucao_parcialmente_gulosa_insercao_mais_barata(pop[j], d, 0.05);
		fo_pop[j] = calcula_fo(pop[j], d)
		
		if (fo_pop[j] < fo_star):
			fo_star = fo_pop[j]
			s_star = pop[j].copy()

	print("Melhor solucao encontrada na construcao: {:f}".format(fo_star))

	ngeracoes = 0
	desvio = float('inf')
	while desvio > max_desvio:
		ngeracoes += 1
		# Aplicar crossover
		quant_filhos = 0
		while quant_filhos < nind/2:			
			# Selecao aleatoria de pais
			jpai1 = np.random.randint(nind/2)
			jpai2 = np.random.randint(nind/2)
			while(jpai1 == jpai2):
				jpai2 = np.random.randint(nind/2)

			if (np.random.random() < prob_crossover):
				'''
				Refinando os pais antes de eles procriarem:
				descida_primeiro_melhora(pop[jpai1],d)
				descida_primeiro_melhora(pop[jpai2],d)
				'''
				if tipo_operador == 1:							
					crossover_OX(pop[jpai1], pop[jpai2], pop[quant_filhos+int(nind/2)], pop[quant_filhos+int(nind/2)+1], n)					
				if tipo_operador == 2:
					crossover_ERX(pop[jpai1], pop[jpai2], pop[quant_filhos+int(nind/2)], pop[quant_filhos+int(nind/2)+1], n)
				
				quant_filhos += 2

		# Aplicar mutacao
		for j in range(nind):		
			if np.random.random() < prob_mutacao:
				mutacao(pop[j], n)

		# Avaliar a populacao inteira (pais e filhos)
		for j in range(nind):
			#print(pop[j])
			fo_pop[j] = calcula_fo(pop[j], d)
			if fo_pop[j] < fo_star:
				fo_star = fo_pop[j]
				s_star = pop[j].copy()
				print("Geracao = {:4d}   fo star = {:10.3f}\n".format(ngeracoes, fo_star))
		#break
		# Definir a populacao sobrevivente
		# fo de todos os individuos da populacao, isto é, pais e filhos
		for j in range(int(nind/2)):
			# escolha dos individuos sobreviventes pelo mecanismo da roleta */
			individuo_escolhido = roleta(nind, fo_pop)			
			'''escolha dos individuos sobreviventes pelo mecanismo da roleta
			   colocando aptidao nula para aqueles que estiverem acima de uma dada
			   faixa, no caso, duas vezes de desvio padrao acima da media '''
			# int individuo_escolhido = roleta_scaling(nind, fo_pop);
			'''for i in range(n):
				pop_sobrev[j][i] = pop[individuo_escolhido][i]'''
			pop_sobrev[j] = pop[individuo_escolhido]

			fo_pop_sobrev[j] = fo_pop[individuo_escolhido]

		# Zerar a populacao e seus dados
		fo_pop = np.zeros(nind, dtype=int) 
		pop = np.zeros((nind, n), dtype=int)

		# Primeira metade da populacao <-- populacao sobrevivente
		for j in range(int(nind/2)):
			for i in range(n):
				pop[j][i] = pop_sobrev[j][i]
			fo_pop[j] = fo_pop_sobrev[j]

		# Zerar a matriz e os vetores que armazenam os dados da populacao sobrevivente
		fo_pop_sobrev = np.zeros(int(nind/2), dtype=int)
		
		# Calcular o desvio padrão das fos da população
		desvio = np.std(fo_pop) # calcula_desvio_padrao(fo_pop,nind/2)

	s = s_star.copy()
	fo = fo_star
	print("Numero de geracoes avaliadas: {:d}".format(ngeracoes))

	return fo, s

# Esta rotina devolve o individuo escolhido pelo mecanismo da roleta
def roleta(nind, fo_pop):
	fracao = np.zeros(nind)
	escala = np.zeros(nind)
	faptidao = np.zeros(nind)
	soma = 0
	fo_min = float('inf')
	fo_max = float('-inf')

	for j in range(nind):
		if fo_pop[j] < fo_min:
			fo_min = fo_pop[j]
		if fo_pop[j] > fo_max:
			fo_max = fo_pop[j]
	# tratar divisao por zero
	tg_alfa = 100 / (fo_max - fo_min)

	for j in range(nind):
		faptidao[j] = tg_alfa * (fo_max - fo_pop[j])
		soma += faptidao[j]

	'''
	for (int j = 0; j < nind; j++){
	printf("faptidao[%3d] = %8.2f  fo_pop[%3d] = %8.2f \n",j,faptidao[j],j,fo_pop[j]);
	}
	'''

	for j in range(nind):
		fracao[j] = faptidao[j] / soma

	escala[0] = fracao[0]

	for j in range(nind):
		escala[j] = escala[j-1] + fracao[j]

	aux = np.random.random()
	j = 0

	while escala[j] < aux:
		j += 1
	escolhido = j

	return escolhido

def mutacao(s, n):
	j = np.random.randint(n)
	i = np.random.randint(n)
	while(i == j):
		i = np.random.randint(n)

	s[j], s[i] = s[i], s[j]

# Operador Crossover OX
def crossover_OX(pai1, pai2, filho1, filho2, n):
	ponto_de_corte_1 = np.random.randint(low=2, high=int((n-1)/2))
	ponto_de_corte_2 = np.random.randint(low=int((n+1)/2),high=n-3)
	
	# Copia os genes entre os 2 pontos de corte em cada filho
	for i in range(ponto_de_corte_1, ponto_de_corte_2+1):
		filho1[i] = pai1[i]
		filho2[i] = pai2[i]

	tam_lista = n - (ponto_de_corte_2 - ponto_de_corte_1 + 1)

	# Cria uma lista com os genes do outro pai a serem inseridos
	lista_pai1 = np.zeros(tam_lista, dtype=int)
	lista_pai2 = np.zeros(tam_lista, dtype=int)

	i = ponto_de_corte_2 + 1
	j = 0

	aux = True
	while aux:
		aux = False
		# procura a cidade pai1[i] no filho2
		existe = False
		for k in range(ponto_de_corte_1, ponto_de_corte_2+1):
			if (filho2[k] == pai1[i]):
				existe = True

		if not existe:
			lista_pai1[j] = pai1[i]
			j += 1
		
		if i == (n-1): 
			i = 0
		else:
			i += 1

		if j < tam_lista:
			aux = True

	i = ponto_de_corte_2 + 1
	j = 0

	aux = True
	while aux:
		aux = False

		# procura a cidade pai2[i] no filho1
		existe = False
		for k in range(ponto_de_corte_1, ponto_de_corte_2+1):
			if filho1[k] == pai2[i]:
				existe = True

		if not existe:
			lista_pai2[j] = pai2[i]
			j += 1		

		if i == (n-1):
			i = 0
		else:
			i += 1

		if j < tam_lista:
			aux = True

	# Completa os genes que faltam
	i = 0
	j = ponto_de_corte_2 + 1
	aux = True
	while aux:
		aux = False

		filho1[j] = lista_pai2[i]
		filho2[j] = lista_pai1[i]
		i += 1
		if j == (n-1):
			j = 0
		else:
			j += 1

		if i < tam_lista:
			aux = True


# Operador Crossover ERX
def crossover_ERX(pai1, pai2, filho1, filho2, n):
	pass

# Esta rotina devolve o individuo escolhido pelo mecanismo da roleta
def roleta_scaling(nind, fo_pop):
	return None