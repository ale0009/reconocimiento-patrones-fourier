"""Pruebas de formas, reproducibilidad e invariancia del descriptor."""

import numpy as np
import pytest
from scipy.ndimage import rotate, shift, zoom

from fourier_patrones.clasificador import distancia
from fourier_patrones.datos import generar_dataset, imagen_base
from fourier_patrones.firmas import firma_imagen
from fourier_patrones.transformadas import fourier_mellin_analitica, remuestrear_log_polar


def test_formas_y_sigma() -> None:
    imagen = imagen_base("A")
    resultado = fourier_mellin_analitica(imagen, forma=(32, 40))
    assert resultado.shape == (32, 40)
    assert firma_imagen(imagen, forma=(32, 40)).shape == (152,)
    with pytest.raises(ValueError):
        remuestrear_log_polar(np.ones((8, 8)), sigma=0)


def test_espectro_hann_centrado_y_logpolar_bilineal() -> None:
    from fourier_patrones.transformadas import espectro_magnitud

    espectro = espectro_magnitud(imagen_base("A"))
    assert espectro.shape == (64, 64)
    assert np.isfinite(espectro).all()
    muestreada = remuestrear_log_polar(espectro, forma=(48, 72))
    assert muestreada.shape == (48, 72)
    assert np.isfinite(muestreada).all()


def test_firma_incluye_bajas_frecuencias_y_marginales_normalizados() -> None:
    firma = firma_imagen(imagen_base("B"), forma=(32, 40))
    assert firma.shape == (152,)
    assert np.linalg.norm(firma) == pytest.approx(1.0)


def test_dataset_admite_varias_referencias_por_clase() -> None:
    conjunto = generar_dataset(semilla=9, referencias_por_clase=3, consultas_por_clase=2)
    assert conjunto.referencias.shape == (30, 64, 64)
    assert conjunto.consultas.shape == (20, 64, 64)


def test_dataset_reproducible() -> None:
    primero, segundo = generar_dataset(semilla=7), generar_dataset(semilla=7)
    np.testing.assert_array_equal(primero.referencias, segundo.referencias)
    np.testing.assert_array_equal(primero.consultas, segundo.consultas)
    assert primero.consultas.shape == (80, 64, 64)


def test_invariancia_aproximada_a_similitud() -> None:
    rng = np.random.default_rng(19)
    base = imagen_base("A")
    otra = imagen_base("B")
    transformada = rotate(base, 73, reshape=False, order=1, mode="constant")
    transformada = zoom(transformada, 1.18, order=1, mode="constant")
    recorte = np.zeros_like(base)
    h, w = transformada.shape
    y, x = max(0, (h - 64) // 2), max(0, (w - 64) // 2)
    pieza = transformada[y : y + min(64, h), x : x + min(64, w)]
    dy, dx = (64 - pieza.shape[0]) // 2, (64 - pieza.shape[1]) // 2
    recorte[dy : dy + pieza.shape[0], dx : dx + pieza.shape[1]] = pieza
    recorte = shift(recorte, (5, -4), mode="constant")
    original_firma = firma_imagen(base)
    misma_firma = firma_imagen(recorte)
    otra_firma = firma_imagen(otra)
    assert distancia(original_firma, misma_firma) < distancia(original_firma, otra_firma)
