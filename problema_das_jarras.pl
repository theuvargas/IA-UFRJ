objetivo((2, _)).

acao((J1, J2), encher1, (4, J2)) :- J1 < 4.
acao((J1, J2), encher2, (J1, 3)) :- J2 < 3.
acao((J1, J2), esvaziar1, (0, J2)) :- J1 > 0.
acao((J1, J2), esvaziar2, (J1, 0)) :- J2 > 0.

% J1+J2 ultrapassa a capacidade de J2
acao((J1, J2), passar12, (J1_novo, 3)) :-
    J1 > 0, J2 < 3,
    J1+J2 > 3,
    J1_novo is J1+J2-3.
% J1+J2 cabe em J1
acao((J1, J2), passar12, (0, J2_novo)) :-
    J1 > 0, J2 < 3,
    J1+J2 =< 3,
    J2_novo is J1+J2.

% J1+J2 ultrapassa a capacidade de J1
acao((J1, J2), passar21, (4, J2_novo)) :-
    J1 < 4, J2 > 0,
    J1+J2 > 4,
    J2_novo is J1+J2-4.
% J1+J2 cabe em J1
acao((J1, J2), passar21, (J1_novo, 0)) :-
    J1 < 4, J2 > 0,
    J1+J2 =< 4,
    J1_novo is J1+J2.

vizinho(N, FilhosN) :-
    findall(X, acao(N, _, X), FilhosN).

add_fronteira_fila(Vizinhos, F1, F2, L) :-
    setdiff(Vizinhos, L, NaoVisitados),
    append(F1, NaoVisitados, F2).

bfs([Vertice | _], Caminho, Final) :-
    objetivo(Vertice), !,
    append(Caminho, [Vertice], Final).
bfs([Vertice | F1], Acc, Caminho) :-
    vizinho(Vertice, Vizinhos),
    append(Acc, [Vertice], L),    
    add_fronteira_fila(Vizinhos, F1, F2, L),
    bfs(F2, L, Caminho).

busca_bfs(Vertices, Caminho) :-
    bfs(Vertices, [], Caminho).

add_fronteira_pilha(Vizinhos, F1, F2, L) :-
    setdiff(Vizinhos, L, NaoVisitados),
    append(NaoVisitados, F1, F2).

dfs([Vertice | _], Caminho, Final) :-
    objetivo(Vertice), !,
    append(Caminho, [Vertice], Final).
dfs([Vertice | F1], Acc, Caminho) :-
    vizinho(Vertice, Vizinhos),
    append(Acc, [Vertice], L),    
    add_fronteira_pilha(Vizinhos, F1, F2, L),
    dfs(F2, L, Caminho).

busca_dfs(Vertices, Caminho) :-
    dfs(Vertices, [], Caminho).

setdiff([],_,[]).
setdiff([H1|T1], S2, Set) :- member(H1, S2), !, setdiff(T1, S2, Set).
setdiff([H1|T1], S2, [H1|Set]) :- setdiff(T1, S2, Set).

% exemplo de chamada: busca_bfs([(0,0)], Caminho)