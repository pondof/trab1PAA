"""Coloração Seletiva de Grafos (SGCP): leitura de instâncias, heurísticas e validação."""

from pathlib import Path


def ler_instancia(caminho):
    """Lê um arquivo no formato p/c/e e devolve a instância como dict.

    Vértices e grupos são numerados a partir de 1; a posição 0 das listas fica sem uso.
    """
    n = m = k = 0
    grupos, grupo_de, adj = [], [], []
    with open(caminho, encoding='utf-8') as arquivo:
        for linha in arquivo:
            partes = linha.split()
            if not partes:
                continue
            if partes[0] == 'p':  # p edge <n> <m> <k>
                n, m, k = int(partes[2]), int(partes[3]), int(partes[4])
                grupos = [[] for _ in range(k + 1)]
                grupo_de = [0] * (n + 1)
                adj = [set() for _ in range(n + 1)]
            elif partes[0] == 'c':  # c <id_grupo> <v1> <v2> ...  (grupo, não comentário)
                g = int(partes[1])
                grupos[g] = [int(v) for v in partes[2:]]
                for v in grupos[g]:
                    grupo_de[v] = g
            elif partes[0] == 'e':  # e <u> <v>
                u, v = int(partes[1]), int(partes[2])
                adj[u].add(v)
                adj[v].add(u)
            # demais linhas (comentários com '#') são ignoradas
    return {'nome': Path(caminho).stem, 'n': n, 'm': m, 'k': k,
            'grupos': grupos, 'grupo_de': grupo_de, 'adj': adj}


def guloso_classes(inst):
    """Guloso por classes de cor: contrata um trabalhador (cor) por vez e dá a ele o
    máximo de tarefas compatíveis, no máximo uma por grupo, começando pelas de menor grau.

    Baseado na heurística gulosa de A. Santini (greedy_heuristic.cpp), que acompanha
    Furini, Malaguti & Santini (2018). Devolve (representantes, cores), com k+1 posições.
    """
    k, adj, grupo_de = inst['k'], inst['adj'], inst['grupo_de']
    ordem = sorted(range(1, inst['n'] + 1), key=lambda v: (len(adj[v]), v))
    representantes = [0] * (k + 1)
    cores = [0] * (k + 1)
    pendentes = set(range(1, k + 1))
    cor = 0
    while pendentes:
        cor += 1               # novo trabalhador
        bloqueados = set()     # vizinhos das tarefas que já estão nesta cor
        for v in ordem:
            g = grupo_de[v]
            if g in pendentes and v not in bloqueados:
                representantes[g] = v
                cores[g] = cor
                pendentes.remove(g)
                bloqueados |= adj[v]
    return representantes, cores


def duas_fases(inst):
    """Baseline: (1) em cada grupo, escolhe o vértice de menor grau (desempate: menor id);
    (2) colore os escolhidos com first-fit, na ordem dos grupos.

    Devolve (representantes, cores), com k+1 posições.
    """
    k, adj = inst['k'], inst['adj']
    representantes = [0] * (k + 1)
    cores = [0] * (k + 1)
    for g in range(1, k + 1):
        representantes[g] = min(inst['grupos'][g], key=lambda v: (len(adj[v]), v))
    for g in range(1, k + 1):
        v = representantes[g]
        usadas = {cores[h] for h in range(1, g) if representantes[h] in adj[v]}
        cor = 1
        while cor in usadas:
            cor += 1
        cores[g] = cor
    return representantes, cores


def validar(inst, representantes, cores):
    """Devolve a lista de erros da solução; lista vazia significa solução válida.

    representantes[g] é o vértice escolhido no grupo g e cores[g] é a sua cor.
    """
    k = inst['k']
    if len(representantes) != k + 1 or len(cores) != k + 1:
        return [f'as listas devem ter k+1 = {k + 1} posições']

    # 1. cada grupo tem um representante, e ele pertence ao grupo
    erros = []
    for g in range(1, k + 1):
        if representantes[g] not in inst['grupos'][g]:
            erros.append(f'grupo {g}: representante {representantes[g]} não pertence ao grupo')
    if erros:
        return erros

    # 2. nenhuma aresta liga dois representantes com a mesma cor
    adj = inst['adj']
    for g in range(1, k + 1):
        for h in range(g + 1, k + 1):
            u, v = representantes[g], representantes[h]
            if cores[g] == cores[h] and v in adj[u]:
                erros.append(f'aresta {u}-{v} (grupos {g} e {h}) com a mesma cor {cores[g]}')
    return erros
