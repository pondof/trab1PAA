"""Execução em lote: roda os dois métodos em todas as instâncias da literatura e gera as tabelas.

Uso (na pasta do projeto): python3 experimentos.py
Gera resultados/tabela.csv (uma linha por instância) e resultados/tabela.md (resumo por conjunto
e tabela completa, prontos para colar no artigo).
"""

import csv
from datetime import datetime
from pathlib import Path

from main import densidade, executar
from sgcp import ler_instancia

REFERENCIAS = Path('instancias', 'referencias.csv')
COLUNAS = ['conjunto', 'instância', 'n', 'm', 'k', 'densidade',
           'cores_baseline', 'cores_guloso', 'tempo_ms', 'válido']
AVISO_RING = ('Em ring, os arquivos ring_n{10,15,20}p1.0s{1..5} são cinco cópias idênticas de três '
              'instâncias (12 arquivos redundantes, como notam Furini, Malaguti & Santini, 2018). '
              'Os arquivos foram mantidos, então as médias de ring contam cada uma dessas três '
              'instâncias cinco vezes.')


def ler_referencias(caminho):
    """Valores da literatura, preenchidos à mão a partir dos artigos: {instância: (valor, fonte)}."""
    if not caminho.is_file():
        return {}
    with open(caminho, encoding='utf-8', newline='') as arquivo:
        return {l['instancia']: (int(l['valor']), l['fonte']) for l in csv.DictReader(arquivo)}


def rodar_tudo(referencias):
    """Roda os dois métodos em cada instância (exceto exemplo/) e devolve uma linha (dict) por instância."""
    linhas = []
    pastas = sorted(p for p in Path('instancias').iterdir() if p.is_dir() and p.name != 'exemplo')
    for pasta in pastas:
        arquivos = sorted(pasta.glob('*.txt'))
        for caminho in arquivos:
            inst = ler_instancia(caminho)
            resultados = executar(inst)
            _, cores_g, ms_g, erros_g = resultados['guloso_classes']
            _, cores_b, _, erros_b = resultados['duas_fases']
            linha = {'conjunto': pasta.name, 'instância': inst['nome'],
                     'n': inst['n'], 'm': inst['m'], 'k': inst['k'], 'densidade': densidade(inst),
                     'cores_baseline': len(set(cores_b[1:])), 'cores_guloso': len(set(cores_g[1:])),
                     'tempo_ms': ms_g, 'válido': not erros_g and not erros_b}
            if referencias:
                valor = referencias.get(inst['nome'], (None, ''))[0]
                linha['literatura'] = valor
                linha['gap'] = None if valor is None else 100 * (linha['cores_guloso'] - valor) / valor
            linhas.append(linha)
        print(f'{pasta.name}: {len(arquivos)} instâncias')
    return linhas


def num(x, casas, virgula):
    """Formata um número com as casas indicadas (vírgula decimal se pedido); None vira vazio."""
    if x is None:
        return ''
    texto = f'{x:.{casas}f}'
    return texto.replace('.', ',') if virgula else texto


def media(linhas, chave):
    return sum(l[chave] for l in linhas) / len(linhas)


def cabecalho(linhas):
    return COLUNAS + (['literatura', 'gap'] if 'literatura' in linhas[0] else [])


def celulas(linha, virgula):
    """Uma linha da tabela completa como lista de textos."""
    c = [linha['conjunto'], linha['instância'], linha['n'], linha['m'], linha['k'],
         num(linha['densidade'], 4, virgula), linha['cores_baseline'], linha['cores_guloso'],
         num(linha['tempo_ms'], 3, virgula), 'sim' if linha['válido'] else 'não']
    if 'literatura' in linha:
        c += [num(linha['literatura'], 0, virgula), num(linha['gap'], 2, virgula)]
    return [str(x) for x in c]


def resumo(linhas):
    """Médias por conjunto, como lista de linhas de texto (a primeira é o cabeçalho)."""
    com_literatura = 'literatura' in linhas[0]
    tabela = [['Conjunto', 'Instâncias', 'n médio', 'k médio', 'Densidade média', 'Cores baseline',
               'Cores guloso', 'Guloso melhor/igual/pior', 'Tempo guloso (ms)', 'Válidas']]
    if com_literatura:
        tabela[0] += ['Com referência', 'Gap médio (%)']
    for conjunto in dict.fromkeys(l['conjunto'] for l in linhas):
        ls = [l for l in linhas if l['conjunto'] == conjunto]
        melhor = sum(l['cores_guloso'] < l['cores_baseline'] for l in ls)
        igual = sum(l['cores_guloso'] == l['cores_baseline'] for l in ls)
        tabela.append([conjunto, str(len(ls)), num(media(ls, 'n'), 1, True), num(media(ls, 'k'), 1, True),
                       num(media(ls, 'densidade'), 4, True), num(media(ls, 'cores_baseline'), 2, True),
                       num(media(ls, 'cores_guloso'), 2, True), f'{melhor}/{igual}/{len(ls) - melhor - igual}',
                       num(media(ls, 'tempo_ms'), 3, True), str(sum(l['válido'] for l in ls))])
        if com_literatura:
            gaps = [l['gap'] for l in ls if l['gap'] is not None]
            tabela[-1] += [str(len(gaps)), num(sum(gaps) / len(gaps), 2, True) if gaps else '']
    return tabela


def tabela_md(tabela):
    """Converte uma lista de linhas (a primeira é o cabeçalho) em linhas de tabela Markdown."""
    texto = ['| ' + ' | '.join(linha) + ' |' for linha in tabela]
    texto.insert(1, '|' + '---|' * len(tabela[0]))
    return texto


def salvar_csv(linhas, caminho):
    with open(caminho, 'w', encoding='utf-8', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalho(linhas))
        escritor.writerows(celulas(l, False) for l in linhas)


def salvar_md(linhas, referencias, caminho):
    texto = ['# Resultados', '',
             f'Gerado por `python3 experimentos.py` em {datetime.now():%Y-%m-%d %H:%M}.', '',
             '- Guloso = `guloso_classes` (método principal); baseline = `duas_fases`.',
             '- Cores = número de cores (trabalhadores) da solução.',
             '- Tempo = tempo do guloso em milissegundos, só o algoritmo, sem a leitura do arquivo.',
             '- Válido = `sim` quando as soluções dos dois métodos passaram pelo validador.']
    if referencias:
        fontes = '; '.join(sorted({fonte for _, fonte in referencias.values()}))
        texto += ['- Literatura = valor de `instancias/referencias.csv`; '
                  'gap = 100 · (cores do guloso − literatura) / literatura.',
                  f'- Fontes dos valores da literatura: {fontes}.']
    texto += ['', '## Resumo por conjunto (médias)', ''] + tabela_md(resumo(linhas))
    if any(l['conjunto'] == 'ring' for l in linhas):
        texto += ['', AVISO_RING]
    texto += ['', '## Todas as instâncias', '']
    texto += tabela_md([cabecalho(linhas)] + [celulas(l, True) for l in linhas])
    caminho.write_text('\n'.join(texto) + '\n', encoding='utf-8')


def main():
    referencias = ler_referencias(REFERENCIAS)
    if not referencias:
        print(f'{REFERENCIAS} não encontrado: tabelas sem as colunas da literatura.')
    linhas = rodar_tudo(referencias)
    sem_instancia = set(referencias) - {l['instância'] for l in linhas}
    if sem_instancia:
        print(f'Aviso: instâncias de {REFERENCIAS} que não existem: {", ".join(sorted(sem_instancia))}')

    Path('resultados').mkdir(exist_ok=True)
    salvar_csv(linhas, Path('resultados', 'tabela.csv'))
    salvar_md(linhas, referencias, Path('resultados', 'tabela.md'))
    print('\n' + '\n'.join(tabela_md(resumo(linhas))))
    print('\nTabelas salvas em resultados/tabela.csv e resultados/tabela.md')


if __name__ == '__main__':
    main()
