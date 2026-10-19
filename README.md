# Coloração Seletiva de Grafos (SGCP)

Trabalho 1 de Projeto e Análise de Algoritmos (BCC 2026.2): heurística construtiva
para a Coloração Seletiva de Grafos, também conhecida como *Partition Coloring
Problem* (PCP).

**Problema.** Dado um grafo G = (V, E) com os vértices divididos em k grupos,
escolher exatamente um vértice (representante) de cada grupo e colorir os
escolhidos com o menor número de cores, sem que dois vizinhos tenham a mesma cor.
Na metáfora do enunciado, os vértices são tarefas, os grupos são categorias, as
arestas ligam tarefas no mesmo horário e as cores são trabalhadores.

## Requisitos

Python 3.9 ou mais recente (testado nas versões 3.9, 3.11 e 3.14). Só a
biblioteca padrão é usada: não há nada para instalar. Os comandos abaixo são
executados na pasta do projeto. No Windows, use `python` (ou `py`) no lugar de
`python3`.

## Como executar

```bash
python3 main.py                              # menu: escolhe o conjunto e depois a instância
python3 main.py instancias/exemplo/toy.txt   # roda direto a instância indicada
python3 experimentos.py                      # roda todas as instâncias e gera as tabelas
python3 -m unittest testes                   # testes com a instância toy
```

`main.py` roda os dois métodos na instância escolhida e mostra um relatório com
os dados da instância, o número de cores e o tempo de cada método, o resultado
da validação e a melhor solução (representante e cor de cada grupo, tarefas de
cada trabalhador) com o seu valor. O mesmo relatório é salvo em
`resultados/<instancia>_<AAAAMMDD-HHMMSS>.txt`.

`experimentos.py` roda os dois métodos em todas as instâncias da literatura e grava
`resultados/tabela.csv` (uma linha por instância) e `resultados/tabela.md` (resumo
por conjunto e tabela completa). Se existir `instancias/referencias.csv`, com as
colunas `instancia,valor,fonte` preenchidas a partir dos artigos, as tabelas ganham
as colunas `literatura` e `gap`.

## Exemplo

Relatório de `python3 main.py instancias/exemplo/toy.txt`. O ótimo da toy é 2
(verificado por força bruta), e o guloso encontra uma solução ótima. Os tempos
variam a cada execução.

```text
Coloração Seletiva de Grafos (SGCP)
Data: 2026-10-16 17:34:54

Instância: toy (instancias/exemplo/toy.txt)
n = 8 vértices, m = 12 arestas, k = 4 grupos, densidade = 0.4286

Método           Cores  Tempo (ms)  Validação
guloso_classes       2       0.010  válida
duas_fases           2       0.007  válida

Melhor solução: guloso_classes
Valor (número de cores = trabalhadores): 2

 Grupo  Representante   Cor
     1              2     1
     2              3     1
     3              6     1
     4              8     2

Tarefas (vértices) de cada trabalhador (cor):
  Trabalhador 1 (3 tarefas): 2, 3, 6
  Trabalhador 2 (1 tarefa): 8
```

## Algoritmos

**Guloso por classes de cor** (`guloso_classes`, método principal). Contrata um
trabalhador por vez e dá a ele o máximo de tarefas compatíveis, no máximo uma por
grupo, percorrendo os vértices em ordem crescente de grau (desempate: menor id).
Quando nenhuma tarefa cabe, contrata outro trabalhador. Baseado na heurística
gulosa do repositório de A. Santini, que acompanha Furini, Malaguti & Santini
(2018). Tempo O(n log n + c·n + m), com c ≤ k cores.

**Duas fases** (`duas_fases`, baseline para comparação). Escolhe em cada grupo o
vértice de menor grau e depois colore os escolhidos com first-fit, na ordem dos
grupos.

Toda solução passa pelo validador (`validar`) antes de ser mostrada ou salva: ele
confere que cada grupo tem um representante do próprio grupo e que nenhuma aresta
liga dois representantes com a mesma cor.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `sgcp.py` | leitura de instância, os dois algoritmos e o validador |
| `main.py` | interface: escolha da instância e relatório |
| `experimentos.py` | execução em lote e tabelas |
| `testes.py` | testes (`unittest`) com a instância toy |
| `instancias/` | casos de teste: `exemplo/` (toy), `random/` (80), `nsfnet/` (50), `ring/` (150) |
| `resultados/` | relatórios e tabelas gerados |
| `relatorio/` | artigo no modelo da SBC (`relatorio.tex`, `referencias.bib`, `sbc-template.sty`, `sbc.bst`); compile com pdfLaTeX e BibTeX, por exemplo no Overleaf |

## Instâncias

As instâncias da literatura vêm do repositório de A. Santini
(<https://github.com/alberto-santini/selective-graph-colouring>, licença GPL-3.0).
Origem, citações e observações estão em [`instancias/README.md`](instancias/README.md).
Formato dos arquivos:

```text
# comentários / metadados
p edge <n> <m> <k>
c <id_grupo> <v1> <v2> ...     # um grupo por linha ("c" é grupo, não comentário)
e <u> <v>                      # uma aresta por linha
```

Vértices e grupos são numerados a partir de 1. Para testar outra instância, basta
criar um arquivo nesse formato e passar o caminho para `main.py`.
