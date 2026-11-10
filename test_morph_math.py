import sys
from pathlib import Path

import pytest

import services

sys.path.insert(0, str(Path(__file__).parent / "modelo-3d"))

from donut import generar_puntos_toro
from taza import generar_puntos_taza


def test_interpolar_en_los_extremos_devuelve_cada_matriz():
    m1 = [[0, 0], [0, 0]]
    m2 = [[1, 2], [3, 4]]

    assert services.interpolar(m1, m2, 0) == [[0, 0], [0, 0]]
    assert services.interpolar(m1, m2, 1) == [[1, 2], [3, 4]]


def test_interpolar_a_la_mitad_promedia():
    m1 = [[0, 0]]
    m2 = [[2, 4]]

    assert services.interpolar(m1, m2, 0.5) == [[1, 2]]


def test_interpolar_dimensiones_distintas_falla():
    with pytest.raises(ValueError):
        services.interpolar([[1, 2]], [[1, 2, 3]], 0.5)


def test_dona_y_taza_tienen_la_misma_cantidad_de_vertices():
    for puntos in (64, 800, 2000):
        dona = generar_puntos_toro(puntos)
        taza = generar_puntos_taza(puntos)
        assert len(dona) == len(taza)


def test_morph_en_t_0_coincide_con_la_dona_y_en_t_1_con_la_taza():
    dona = generar_puntos_toro(100)
    taza = generar_puntos_taza(100)

    assert services.interpolar(dona, taza, 0) == dona
    assert services.interpolar(dona, taza, 1) == taza
