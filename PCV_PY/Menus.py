'''
Menu principal
'''
def menu_principal():
    while True:
        print("*******************Menu Principal************************* ")
        print("ATENCAO: Necessario gerar solucao inicial antes de refinar")
        print("                1. Gere solucao inicial ")
        print("                2. Descida com Best Improvement")
        print("                3. Descida randomica ")
        print("                4. Descida com Primeiro de Melhora (First Improvement) ")
        print("                5. Multi-Start ")
        print("                6. Simulated Annealing ")
        print("                7. Busca Tabu ")
        print("                8. ILS ")
        print("                9. GRASP ")
        print("               10. VND ")
        print("               11. VNS ")
        print("               12. Algoritmos Geneticos ")
        print("               13. Algoritmos Memeticos ")
        print("               14. Colonia de Formigas ")
        print("                0. Sair ")
        escolha = input('Escolha: ')
        escolha = int(escolha)
        if escolha >= 0 or escolha <= 14:
            break
    return escolha
        
'''
Menu de geracao de uma solucao inicial
'''
def menu_solucao_inicial():
    while True:
        print("************Geracao da Solucao Inicial**************** ")
        print("                1. Gulosa (Vizinho mais proximo) ")
        print("                2. Parcialmente gulosa (Vizinho mais proximo) ")
        print("                3. Gulosa (Insercao Mais Barata) ")
        print("                4. Parcialmente gulosa (Insercao Mais Barata) ")
        print("                5. Aleatoria ")
        print("                0. Voltar ")
        escolha = input('Escolha: ')
        escolha = int(escolha)
        if escolha >= 0 or escolha <= 5:
            break
    return escolha

'''
Menu GRASP
'''
def menu_GRASP():
    while True:
        print("*******************Menu GRASP************************* ")
        print("                1. Vizinho Mais Proximo ")
        print("                2. Insercao Mais Barata ")
        print("                0. Voltar ")
        escolha = input('Escolha: ')
        escolha = int(escolha)
        if escolha >= 0 or escolha <= 2:
            break
    return escolha

'''
Menu Algoritmos Geneticos
'''
def menu_AG():
    while True:
        print("****************Menu Algoritmos Geneticos********************** ")
        print("                1. Operador OX ")
        print("                2. Operador ERX ")
        print("                0. Voltar ")
        escolha = input('Escolha: ')
        escolha = int(escolha)
        if escolha >= 0 or escolha <= 2:
            break
    return escolha

