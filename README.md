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

Python 3.10 ou mais recente. Só a biblioteca padrão é usada: não há nada para
instalar. Os comandos abaixo são executados na pasta do projeto.

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

`experimentos.py` grava `resultados/tabela.csv` e `resultados/tabela.md`.

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
