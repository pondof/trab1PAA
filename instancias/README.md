# Instâncias

Benchmark clássico da Coloração Seletiva de Grafos (SGCP), também conhecida como
*Partition Coloring Problem* (PCP).

| Pasta | Instâncias | n | k | Densidade | Origem |
|---|---:|---|---|---|---|
| `exemplo/` | 1 | 8 | 4 | 0,43 | `toy.txt`, construída à mão (ótimo = 2) |
| `random/` | 80 | 20–120 | 10–60 | 0,10–0,91 | Frota et al. (2010), grafos aleatórios |
| `nsfnet/` | 50 | 16–257 | 12–182 | 0,09–0,13 | Li & Simha (2000), rede NSF (roteamento e atribuição de comprimentos de onda) |
| `ring/` | 150 | 8–760 | 4–380 | 0,36–0,41 | Frota et al. (2010), redes em anel (roteamento e atribuição de comprimentos de onda) |

## Origem

Os arquivos de `random/`, `nsfnet/` e `ring/` vêm do repositório de A. Santini,
[`alberto-santini/selective-graph-colouring`](https://github.com/alberto-santini/selective-graph-colouring),
no commit `731f99db29d5d20de9dc83ffada9f418b93100cf`, que acompanha
Furini, Malaguti & Santini (2018). O conjunto também foi distribuído pelo grupo
de C. C. Ribeiro (<http://www2.ic.uff.br/~celso/grupo/pcp.htm>).

Eles foram convertidos para o formato abaixo, com vértices e grupos numerados a
partir de 1. Cada arquivo guarda nos comentários o conjunto, o arquivo de
origem, o repositório e o commit.

## Formato

```text
# comentários / metadados (# chave: valor)
p edge <n> <m> <k>
c <id_grupo> <v1> <v2> ...     # um grupo por linha ("c" é grupo, não comentário)
e <u> <v>                      # uma aresta por linha
```

## Valores de referência

`referencias.csv` traz, para 187 arquivos, o valor ótimo ou o melhor conhecido
(colunas `instancia`, `valor`, `otimo`, `fonte`), tirado das Tabelas 2 e 3 de
Furini, Malaguti & Santini (2018), que também reproduzem os limites de Hoshino,
Frota & de Souza (2011). Em 180 arquivos o valor é ótimo (`otimo = sim`); em 7
(`n90p2t2s4`, `n90p3t2s4` e as cinco cópias de `ring_n20p1.0s1`) é o melhor
limite superior conhecido. Os demais arquivos não aparecem nas tabelas do artigo.
O `experimentos.py` usa esse arquivo para calcular o gap.

Para conferir que as instâncias são as mesmas do artigo: o `n` coincide em
todas, e o `|E|` do artigo, que conta as arestas depois de transformar cada
grupo em uma clique, coincide em 174 das 175 instâncias. A exceção é
`n90p2t2s2` (837 aqui, 821 no artigo, o mesmo valor de `n90p2t2s4`),
provavelmente um erro de digitação.

## Observações

- Os grupos têm 2 vértices em `random/` e `ring/`, e 1 ou 2 vértices em `nsfnet/`.
- `random/` e `nsfnet/` têm arestas entre vértices do mesmo grupo. Como só um
  vértice de cada grupo é escolhido, essas arestas nunca entram na solução.
- **Duplicatas em `ring/`:** em cada um dos três grupos de arquivos
  `ring_n{10,15,20}p1.0s{1..5}`, os cinco arquivos têm conteúdo idêntico, a menos
  dos comentários. São 3 instâncias distintas em 15 arquivos, ou seja, 12
  arquivos redundantes, como já notam Furini, Malaguti & Santini (2018, §5.1).
  Os arquivos foram mantidos para preservar os nomes originais. Nas médias,
  lembre que esses casos aparecem cinco vezes.

## Licença e citação

O repositório de origem é distribuído sob a **GNU GPL v3.0**. As instâncias são
redistribuídas aqui, convertidas, com atribuição. Ao usá-las, cite:

- F. Furini, E. Malaguti, A. Santini. *An exact algorithm for the Partition
  Coloring Problem*. Computers & Operations Research 92:170–181, 2018.
  doi:10.1016/j.cor.2017.12.019
- Y. Frota, N. Maculan, T. F. Noronha, C. C. Ribeiro. *A branch-and-cut
  algorithm for partition coloring*. Networks 55(3):194–204, 2010.
- G. Li, R. Simha. *The partition coloring problem and its application to
  wavelength routing and assignment*. Proc. 1st Workshop on Optical Networks, 2000.
