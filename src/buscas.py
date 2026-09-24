"""BFS, DFS, UCS e A* sobre a grade do pomar."""
from collections import deque
import heapq
from gerador_pomar import CUSTO, BLOQUEADO

ORDEM = ((-1, 0), (1, 0), (0, -1), (0, 1))  # Norte, Sul, Oeste, Leste


def vizinhos(mapa, no):
    r, c = no
    for dr, dc in ORDEM:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nr][nc] != BLOQUEADO:
            yield (nr, nc)


def _resultado(pais, custos, destino, expandidos, fronteira_max):
    if destino not in pais:
        caminho = []
        custo = None
    else:
        caminho, no = [], destino
        while no is not None:
            caminho.append(no); no = pais[no]
        caminho.reverse(); custo = custos[destino]
    return {"caminho": caminho, "custo": custo, "passos": max(0, len(caminho)-1),
            "nos_expandidos": expandidos, "fronteira_max": fronteira_max}


def bfs(mapa):
    origem, destino = (0, 0), (len(mapa)-1, len(mapa[0])-1)
    q, pais, custos = deque([origem]), {origem: None}, {origem: 0}
    exp = 0; fmax = 1
    while q:
        atual = q.popleft(); exp += 1
        if atual == destino: break
        for novo in vizinhos(mapa, atual):
            if novo not in pais:
                pais[novo] = atual; custos[novo] = custos[atual] + CUSTO[mapa[novo[0]][novo[1]]]; q.append(novo)
        fmax = max(fmax, len(q))
    return _resultado(pais, custos, destino, exp, fmax)


def dfs(mapa):
    origem, destino = (0, 0), (len(mapa)-1, len(mapa[0])-1)
    pilha, pais, custos = [origem], {origem: None}, {origem: 0}
    exp = 0; fmax = 1
    while pilha:
        atual = pilha.pop(); exp += 1
        if atual == destino: break
        for novo in vizinhos(mapa, atual):
            if novo not in pais:
                pais[novo] = atual; custos[novo] = custos[atual] + CUSTO[mapa[novo[0]][novo[1]]]; pilha.append(novo)
        fmax = max(fmax, len(pilha))
    return _resultado(pais, custos, destino, exp, fmax)


def ucs(mapa):
    origem, destino = (0, 0), (len(mapa)-1, len(mapa[0])-1)
    fila, pais, dist = [(0, 0, origem)], {origem: None}, {origem: 0}
    exp = 0; fmax = 1; contador = 1
    while fila:
        custo, _, atual = heapq.heappop(fila)
        if custo != dist[atual]: continue
        exp += 1
        if atual == destino: break
        for novo in vizinhos(mapa, atual):
            nc = custo + CUSTO[mapa[novo[0]][novo[1]]]
            if nc < dist.get(novo, float("inf")):
                dist[novo] = nc; pais[novo] = atual; contador += 1
                heapq.heappush(fila, (nc, contador, novo))
        fmax = max(fmax, len(fila))
    return _resultado(pais, dist, destino, exp, fmax)


def h1(no, destino): return 0
def h2(no, destino): return abs(no[0]-destino[0]) + abs(no[1]-destino[1])
def h3(no, destino): return 4 * h2(no, destino)


def astar(mapa, heuristica=h2):
    origem, destino = (0, 0), (len(mapa)-1, len(mapa[0])-1)
    fila, pais, dist = [(heuristica(origem, destino), 0, 0, origem)], {origem: None}, {origem: 0}
    exp = 0; fmax = 1; contador = 1
    while fila:
        prioridade, custo_atual, _, atual = heapq.heappop(fila)
        if custo_atual != dist.get(atual): continue
        exp += 1
        if atual == destino: break
        for novo in vizinhos(mapa, atual):
            nc = dist[atual] + CUSTO[mapa[novo[0]][novo[1]]]
            if nc < dist.get(novo, float("inf")):
                dist[novo] = nc; pais[novo] = atual; contador += 1
                heapq.heappush(fila, (nc + heuristica(novo, destino), nc, contador, novo))
        fmax = max(fmax, len(fila))
    return _resultado(pais, dist, destino, exp, fmax)


busca_largura = bfs; busca_profundidade = dfs
busca_custo_uniforme = ucs; busca_a_estrela = astar
busca_bfs = bfs; busca_dfs = dfs; busca_ucs = ucs; busca_astar = astar
