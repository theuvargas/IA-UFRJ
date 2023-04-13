from random import randint, choice, random, shuffle
from matplotlib import pyplot as plt
from statistics import mean
from copy import deepcopy
from timeit import default_timer as timer
import sys

def todos_vizinhos(tabuleiro: list):
    '''
    Retorna todos os (N - 1) * N vizinhos, que sao obtidos
    após realizar um movimento de rainha na coluna a qual
    ela pertence
    '''
    
    vizinhos = []

    # percorre as N colunas
    for i in range(len(tabuleiro)):
        # para cada coluna, gera as (N - 1) posicoes vizinhas
        for j in range(len(tabuleiro)):
            novo_tabuleiro = tabuleiro.copy()
            if (j != tabuleiro[i]):
                novo_tabuleiro[i] = j
                vizinhos.append(novo_tabuleiro)              
            
    return vizinhos

def gerador_vizinhos(tabuleiro: list):
    '''
    Retorna todos os (N - 1) * N vizinhos, que sao obtidos
    após realizar um movimento de rainha na coluna a qual
    ela pertence
    '''
                
    i = 0
    while i < len(tabuleiro):
        j = 0
        while j < len(tabuleiro):
            novo_tabuleiro = tabuleiro.copy()
            if (j != tabuleiro[i]):
                novo_tabuleiro[i] = j
                tabuleiro_alterado = (yield novo_tabuleiro)

                if tabuleiro_alterado:
                    tabuleiro = tabuleiro_alterado
                    i, j = -1, 0
                    yield # isso é necessário senão o próximo tabuleiro é perdido
                    break
            j += 1
        i += 1
        
            

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

    return 1/(1+ataques_tabuleiro(tabuleiro))

def inversa_f(score):
    return round((1 / score) - 1)

def imprime_tabuleiro(tabuleiro: list):
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro)):
            if (i == tabuleiro[j]):
                print(" 1 ", end="")
            else:
                print(" 0 ", end="")
        print()

def hill_climbing_primeira(n: int):
    tabuleiro = gera_tabuleiros(1, n)[0]
    maior_score = f(tabuleiro)

    dados = {'iteração': [0], 'melhor': [maior_score]}

    gerador = gerador_vizinhos(tabuleiro)
    i = 1
    for vizinho in gerador:
        score_vizinho = f(vizinho)
        if score_vizinho > maior_score:
            maior_score = score_vizinho
            tabuleiro = vizinho
            gerador.send(vizinho)

            dados["iteração"].append(i)
            i += 1
            dados["melhor"].append(maior_score)

        if maior_score == 1:
            break

    return (tabuleiro, maior_score, dados)

def hill_climbing_melhor(n: int):
    tabuleiro = gera_tabuleiros(1, n)[0]
    maior_score = f(tabuleiro)

    dados = {'iteração': [], 'melhor': []}

    i = 0
    while True:
        vizinhos = todos_vizinhos(tabuleiro)
        scores_vizinhos = list(map(f, vizinhos))

        score_melhor_vizinho = max(scores_vizinhos)

        if score_melhor_vizinho <= maior_score:
            break

        indice_melhor = scores_vizinhos.index(score_melhor_vizinho)
        tabuleiro = vizinhos[indice_melhor]
        maior_score = score_melhor_vizinho

        dados["iteração"].append(i)
        i += 1
        dados["melhor"].append(maior_score)

        if maior_score == 1:
            break

    return (tabuleiro, maior_score, dados)

def main():
    if len(sys.argv) < 2:
        print(f"Execute como: {sys.argv[0]} <N>")
        exit(1)

    n = int(sys.argv[1])

    inicio = timer()
    tabuleiro, score, dados = hill_climbing_primeira(n)
    tempo = timer() - inicio

    inicio = timer()
    tabuleiro2, score2, dados2 = hill_climbing_melhor(n)
    tempo2 = timer() - inicio
    
    fig, ax = plt.subplots()
    ax.plot(dados["iteração"], dados["melhor"], label="Primeira escolha")
    ax.plot(dados2["iteração"], dados2["melhor"], label="Melhor escolha")
    ax.set_xlabel('Iteração')
    ax.set_ylabel('Score')
    ax.legend()
    ax.set_title(f'{n} Rainhas')

    fig.show()

    print('---------------------------------------------------------')
    print('Primeira escolha:')
    print(tabuleiro, score, tempo)
    print('\nMelhor escolha:')
    print(tabuleiro2, score2, tempo2)

    input()

if __name__ == "__main__":
    main()
