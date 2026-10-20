"""Interface: escolhe uma instância, roda os dois métodos, mostra e salva o relatório."""

import sys
import time
from datetime import datetime
from pathlib import Path

from sgcp import ler_instancia, guloso_classes, duas_fases, validar

CONJUNTOS = ['exemplo', 'random', 'nsfnet', 'ring']
METODOS = {'guloso_classes': guloso_classes, 'duas_fases': duas_fases}


def escolher(titulo, opcoes):
    """Mostra as opções numeradas e devolve a escolhida."""
    print(f'\n{titulo}')
    for i, opcao in enumerate(opcoes, 1):
        print(f'  {i:3}. {opcao}')
    while True:
        resposta = input('Número: ').strip()
        if resposta.isdigit() and 1 <= int(resposta) <= len(opcoes):
            return opcoes[int(resposta) - 1]
        print(f'Digite um número de 1 a {len(opcoes)}.')


def menu():
    """Menu em dois níveis: conjunto e depois instância. Devolve o caminho do arquivo."""
    conjunto = escolher('Conjunto de instâncias:', CONJUNTOS)
    arquivos = sorted(Path('instancias', conjunto).glob('*.txt'))
    nome = escolher(f'Instâncias de {conjunto}:', [a.stem for a in arquivos])
    return Path('instancias', conjunto, nome + '.txt')


def executar(inst):
    """Roda e valida cada método. Só o algoritmo é cronometrado, sem a leitura do arquivo."""
    resultados = {}
    for nome, metodo in METODOS.items():
        inicio = time.perf_counter()
        representantes, cores = metodo(inst)
        ms = (time.perf_counter() - inicio) * 1000
        erros = validar(inst, representantes, cores)
        resultados[nome] = (representantes, cores, ms, erros)
    return resultados


def densidade(inst):
    """Densidade do grafo: 2m / (n(n-1))."""
    n, m = inst['n'], inst['m']
    return 2 * m / (n * (n - 1)) if n > 1 else 0


def relatorio(caminho, inst, resultados):
    """Monta o texto do relatório."""
    n, m, k = inst['n'], inst['m'], inst['k']
    linhas = [
        'Coloração Seletiva de Grafos (SGCP)',
        f'Data: {datetime.now():%Y-%m-%d %H:%M:%S}',
        '',
        f'Instância: {inst["nome"]} ({caminho})',
        f'n = {n} vértices, m = {m} arestas, k = {k} grupos, densidade = {densidade(inst):.4f}',
        '',
        f'{"Método":<16}{"Cores":>6}{"Tempo (ms)":>12}  Validação',
    ]
    for nome, (_, cores, ms, erros) in resultados.items():
        status = 'válida' if not erros else f'INVÁLIDA ({len(erros)} erros; 1º: {erros[0]})'
        linhas.append(f'{nome:<16}{len(set(cores[1:])):>6}{ms:>12.3f}  {status}')

    validos = [nome for nome, (_, _, _, erros) in resultados.items() if not erros]
    if not validos:
        linhas += ['', 'Nenhum método produziu solução válida.']
        return '\n'.join(linhas)

    # melhor solução: a válida com menos cores; no empate, a do guloso (primeiro método)
    melhor = min(validos, key=lambda nome: len(set(resultados[nome][1][1:])))
    representantes, cores = resultados[melhor][0], resultados[melhor][1]
    valor = len(set(cores[1:]))
    linhas += ['', f'Melhor solução: {melhor}', f'Valor (número de cores = trabalhadores): {valor}',
               '', f'{"Grupo":>6}{"Representante":>15}{"Cor":>6}']
    for g in range(1, k + 1):
        linhas.append(f'{g:>6}{representantes[g]:>15}{cores[g]:>6}')

    linhas += ['', 'Tarefas (vértices) de cada trabalhador (cor):']
    tarefas = {}
    for g in range(1, k + 1):
        tarefas.setdefault(cores[g], []).append(representantes[g])
    for cor in sorted(tarefas):
        qtd = len(tarefas[cor])
        lista = ', '.join(str(v) for v in tarefas[cor])
        linhas.append(f'  Trabalhador {cor} ({qtd} {"tarefa" if qtd == 1 else "tarefas"}): {lista}')
    return '\n'.join(linhas)


def main():
    if len(sys.argv) > 1:
        caminho = Path(sys.argv[1])
        if not caminho.is_file():
            sys.exit(f'Arquivo não encontrado: {caminho}')
    else:
        caminho = menu()

    inst = ler_instancia(caminho)
    texto = relatorio(caminho, inst, executar(inst))
    print('\n' + texto)

    Path('resultados').mkdir(exist_ok=True)
    saida = Path('resultados', f'{inst["nome"]}_{datetime.now():%Y%m%d-%H%M%S}.txt')
    saida.write_text(texto + '\n', encoding='utf-8')
    print(f'\nRelatório salvo em {saida}')


if __name__ == '__main__':
    main()
