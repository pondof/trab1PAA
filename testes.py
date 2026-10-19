"""Testes com a instância toy (8 vértices, 4 grupos, ótimo = 2). Rode: python3 -m unittest testes"""

import itertools
import unittest
from pathlib import Path

from sgcp import ler_instancia, guloso_classes, duas_fases, validar

TOY = Path(__file__).parent / 'instancias' / 'exemplo' / 'toy.txt'


class TestesToy(unittest.TestCase):

    def setUp(self):
        self.inst = ler_instancia(TOY)

    def test_leitura(self):
        self.assertEqual((self.inst['n'], self.inst['m'], self.inst['k']), (8, 12, 4))
        self.assertEqual(self.inst['grupos'][1:], [[1, 2], [3, 4], [5, 6], [7, 8]])
        self.assertEqual(self.inst['grupo_de'][1:], [1, 1, 2, 2, 3, 3, 4, 4])
        self.assertEqual(self.inst['adj'][2], {4, 5})

    def test_guloso_valido_com_2_cores(self):
        representantes, cores = guloso_classes(self.inst)
        self.assertEqual(validar(self.inst, representantes, cores), [])
        self.assertEqual(len(set(cores[1:])), 2)

    def test_duas_fases_valido(self):
        representantes, cores = duas_fases(self.inst)
        self.assertEqual(validar(self.inst, representantes, cores), [])

    def test_validador_aceita_otimo(self):
        self.assertEqual(validar(self.inst, [0, 2, 4, 6, 8], [0, 1, 2, 1, 2]), [])

    def test_validador_recusa_aresta_com_mesma_cor(self):
        # 1, 3, 5 e 7 formam um K4: duas cores não bastam
        self.assertNotEqual(validar(self.inst, [0, 1, 3, 5, 7], [0, 1, 2, 1, 2]), [])

    def test_validador_recusa_representante_fora_do_grupo(self):
        # o vértice 3 é do grupo 2, não do grupo 1
        self.assertNotEqual(validar(self.inst, [0, 3, 4, 6, 8], [0, 1, 2, 1, 2]), [])

    def test_otimo_da_toy_e_2_por_forca_bruta(self):
        # todas as 16 seleções e todas as colorações com até k cores
        k = self.inst['k']
        melhor = min(len(set(cores))
                     for selecao in itertools.product(*self.inst['grupos'][1:])
                     for cores in itertools.product(range(1, k + 1), repeat=k)
                     if not validar(self.inst, [0, *selecao], [0, *cores]))
        self.assertEqual(melhor, 2)


if __name__ == '__main__':
    unittest.main()
