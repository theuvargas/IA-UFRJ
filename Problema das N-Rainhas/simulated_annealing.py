from random import randint, choice, random, shuffle
from matplotlib import pyplot as plt
from statistics import mean
from copy import deepcopy
from timeit import default_timer as timer
import sys
from math import exp

def um_vizinho(tabuleiro: list):
    '''
    Escolhe aleatoriamente um dentre todos os vizinhos de um tabuleiro
    '''
    
    coluna_aleatoria = randint(0, len(tabuleiro) - 1)
    novo_tabuleiro = tabuleiro.copy()
    novo_tabuleiro[coluna_aleatoria] = choice(outras_posicoes(tabuleiro[coluna_aleatoria], len(tabuleiro)))  
    
    return novo_tabuleiro

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

def gera_tabuleiros(tam_pop: int, n: int):
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

    return ataques_tabuleiro(tabuleiro)

def imprime_tabuleiro(tabuleiro: list):
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro)):
            if (i == tabuleiro[j]):
                print(" 1 ", end="")
            else:
                print(" 0 ", end="")
        print()

def simulated_annealing(n, temperatura, alpha, max_iter):
    tabuleiro = gera_tabuleiros(1, n)[0]
    dados = {'iteração': [], 'ataques': []}
    score_atual = f(tabuleiro)

    for i in range(max_iter):

        dados["iteração"].append(i)
        dados["ataques"].append(score_atual)
        
        if temperatura == 0:
            print('caco')

        if score_atual == 0.0:
            break

        vizinho = um_vizinho(tabuleiro)
        score_vizinho = f(vizinho)

        delta = score_vizinho - score_atual

        if delta <= 0:
            tabuleiro = vizinho
            score_atual = score_vizinho
        else:
            n = random()
            e = -delta/temperatura
            #print(exp(e))
            if n < exp(e):
                tabuleiro = vizinho
                score_atual = score_vizinho
        
        temperatura *= alpha

    return (tabuleiro, score_atual, dados)

def main():
    if len(sys.argv) <= 4:
        print(f"Execute como: {sys.argv[0]} <N> <Temperatura> <Alpha> <Iterações>")
        exit(1)

    n = int(sys.argv[1])
    temperatura = int(sys.argv[2])
    alpha = float(sys.argv[3])
    max_iter = int(sys.argv[4])

    inicio = timer()
    tabuleiro, score, dados = simulated_annealing(n, temperatura, alpha, max_iter)
    tempo = timer() - inicio
    
    fig, ax = plt.subplots()
    ax.plot(dados["iteração"], dados["ataques"])
    ax.set_xlabel('Iteração')
    ax.set_ylabel('Ataques')
    ax.set_title(f'{n} Rainhas')

    fig.show()

    print('---------------------------------------------------------')
    print(tabuleiro, score, tempo)

    input()

if __name__ == "__main__":
    main()
