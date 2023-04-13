from random import randint, choice, random, shuffle
from matplotlib import pyplot as plt
from statistics import mean
from copy import deepcopy
from timeit import default_timer as timer
import sys

def outras_posicoes(pos: int, n: int):
    '''
    Dada uma coluna, com rainha na linha pos, retorna todas
    as outras linhas disponíveis
    '''

    posicoes = []

    for i in range(n):
        if i == pos:
            continue

        posicoes.append(i)

    return posicoes

def gera_individuos(tam_pop: int, n: int):
    '''
    Retorna tam_pop indivíduos (tabuleiros) gerados aleatoriamente
    '''

    tabuleiros:list = []
    for i in range(tam_pop):
        tabuleiro:list = []
        for j in range(n):
            tabuleiro.append(randint(0, n-1))
        tabuleiros.append(tabuleiro)

    return tabuleiros

def max_ataques(n):
    return int((n) * (n - 1) / 2)

# https://towardsdatascience.com/computing-number-of-conflicting-pairs-in-a-n-queen-board-in-linear-time-and-space-complexity-e9554c0e0645
def ataques_tabuleiro(tabuleiro: list):
    n = len(tabuleiro)

    freq_linha = [0] * n
    freq_diag_principal = [0] * (2 * n)
    freq_diag_secundaria = [0] * (2 * n)

    for i in range(n):
        freq_linha[tabuleiro[i]] += 1
        freq_diag_principal[tabuleiro[i] + i] += 1
        freq_diag_secundaria[n - tabuleiro[i] + i] += 1

    conflitos = 0
    
    for i in range(2 * n):
        if (i < n):
            conflitos += max_ataques(freq_linha[i])
        conflitos += max_ataques(freq_diag_principal[i])
        conflitos += max_ataques(freq_diag_secundaria[i])
    return int(conflitos)

def f(tabuleiro):
    '''
    Função de avaliação de um tabuleiro
    '''

    return 1/(1+ataques_tabuleiro(tabuleiro))

def cria_roleta_viciada(scores: list):
    # divide o score de cada tabuleiro pelo score total dos tabuleiros,
    # resultando nas porcentagens
    total_scores = sum(scores)
    porcentagens = [scr/total_scores for scr in scores]

    # roleta com porcentagens acumuladas
    roleta = [0.0]
    soma = 0
    for pct in porcentagens:
        roleta.append(soma + pct)
        soma += pct

    return roleta

def selecao(individuos: list, scores: list):
    '''
    Seleciona os indivíduos que farão parte da população intermediária (mating pool)
    '''
    roleta = cria_roleta_viciada(scores)  

    selecionados = []
    for individuo in individuos:
        num = random()
        for i in range(0, len(roleta) - 1):
            # se o número aleatório estiver no intervalo [i, i + 1), seleciona o tabuleiro correspondente
            if roleta[i] <= num and num < roleta[i + 1]:
                selecionados.append(individuos[i])
                break

    return selecionados


def crossover(pop_intermediaria: list, probabilidade_crossover: float, tam_pop):
    '''
    A partir de um ponto de corte gerado aleatoriamente, mistura os indivíduos (tabuleiros)
    cruzando suas informações genéticas tomadas dois a dois e retorna a nova população
    '''

    n = len(pop_intermediaria[0]) # dimensão de cada tabuleiro
    nova_geracao = []

    shuffle(pop_intermediaria)
    while (len(nova_geracao) < tam_pop):
        pai1 = pop_intermediaria.pop()
        pai2 = pop_intermediaria.pop()

        num = random()

        if (num < probabilidade_crossover):
            ponto_de_corte = randint(1, n - 1)

            nova_geracao.append(pai1[:ponto_de_corte] + pai2[ponto_de_corte:])
            nova_geracao.append(pai2[:ponto_de_corte] + pai1[ponto_de_corte:])

        else:
            nova_geracao.append(pai1)
            nova_geracao.append(pai2)
    
    return nova_geracao


def mutacao(individuos: list, probabilidade_mutacao: float):
    '''
    Faz um movimento aleatório em cada coluna de todos os indivíduos com probabilidade 
    igual a "probabilidade_mutacao"
    '''
    
    n = len(individuos[0]) # dimensão de cada tabuleiro
    
    for ind in individuos:
        for i in range(n):
            num = random()

            if num < probabilidade_mutacao:
                #ind[i] = randint(0, n - 1)
                ind[i] = choice(outras_posicoes(ind[i], n))


def imprime_tabuleiro(tabuleiro: list):
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro)):
            if (i == tabuleiro[j]):
                print(" 1 ", end="")
            else:
                print(" 0 ", end="")
        print()
            

def seleciona_elite(individuos: list, scores: list, tam_elite: int):
    '''
    Percorre a lista de indivíduos e retorna uma lista com os de melhor score
    '''
    
    elite = []

    for i in range(tam_elite):
        indice_max = scores.index(max(scores))
        scores.pop(indice_max)
        melhor = individuos.pop(indice_max)
        elite.append(melhor)
    
    return elite

def algoritmo_genetico(tam_tabuleiro: int, num_geracoes: int, tam_pop: int, prob_crossover: float, prob_mutacao: float, elitismo: float):
    tam_elite = int(tam_pop * elitismo)
    if tam_elite % 2 == 1:
        tam_elite += 1

    individuos = gera_individuos(tam_pop, tam_tabuleiro)

    inicio = timer()
    intervalo = 0 # timer

    dados = {'geração': [], 'melhor': [], 'média': [], 'pior': []}

    for i in range(num_geracoes):
        scores = list(map(f, individuos))
        
        tempo = timer() - inicio
        if (tempo > intervalo):
            print(f'{intervalo // 60} minutos\t\tgerações: {i}\t\tmelhor: {inversa_f(max(scores))} ataques\t\tpior: {inversa_f(min(scores))} ataques')
            intervalo += 60

        maior = max(scores)
        dados["geração"].append(i)
        dados["melhor"].append(maior)
        dados["média"].append(mean(scores))
        dados["pior"].append(min(scores))

        if maior == 1:
            break

        elite = seleciona_elite(individuos, scores, tam_elite)

        pop_intermediaria = selecao(individuos, scores)
        
        elite_copia = deepcopy(elite)
        pop_intermediaria.extend(elite)
        individuos = crossover(pop_intermediaria, prob_crossover, tam_pop - tam_elite)

        mutacao(individuos, prob_mutacao)

        individuos.extend(elite_copia)
    
    print(f"Indivíduos: {len(individuos)}")
    print(f"Elite: {tam_elite}")
    
    melhor = [0] * tam_pop
    for ind in individuos:
        if f(ind) > f(melhor):
            melhor = ind
    
    return (melhor, f(melhor), dados)

def inversa_f(score):
    return round((1 / score) - 1)

def main():
    if len(sys.argv) < 7:
        print(f"Execute como: {sys.argv[0]}")
        print("\t<N>")
        print("\t<limite máximo de gerações (ordem de grandeza)>")
        print("\t<número de indivíduos>") 
        print("\t<probilidade de crossover>")
        print("\t<probabilidade de mutação> ")
        print("\t<percentual de indivíduos que farão parte da elite>")
        exit(1)

    #_, individuos, n, ordem_grandeza, prob_crossover, prob_mutacao, taxa_elite = sys.argv
    n = int(sys.argv[1])
    ordem_grandeza = int(sys.argv[2])
    individuos = int(sys.argv[3])
    prob_crossover = float(sys.argv[4])
    prob_mutacao = float(sys.argv[5])
    taxa_elite = float(sys.argv[6])

    inicio = timer()
    tabuleiro, score, dados = algoritmo_genetico(n, 10**ordem_grandeza, individuos, prob_crossover, prob_mutacao, taxa_elite)
    tempo = timer() - inicio
    
    fig, ax = plt.subplots()
    ax.plot(dados["geração"], dados["melhor"], label="Melhor", color="seagreen")
    ax.plot(dados["geração"], dados["média"], label="Média", color="steelblue")
    ax.plot(dados["geração"], dados["pior"], label="Pior", color="red")
    ax.set_xlabel('Gerações')
    ax.set_ylabel('Score')
    ax.legend()
    ax.set_title(f'Tabuleiro {n} x {n}')

    fig.show()

    print('---------------------------------------------------------')
    print(tabuleiro, score)
    print()

    geracoes = len(dados["geração"])
    print(f'{geracoes} gerações em {int(tempo // 60)} minutos e {round(tempo % 60)} segundos ({round(geracoes / (tempo / 60), 2)} gerações por minuto)')

    input()

if __name__ == "__main__":
    main()
