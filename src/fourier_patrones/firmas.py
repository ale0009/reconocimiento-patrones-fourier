"""Firmas 1D normalizadas derivadas de los marginales de una matriz."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def normalizar(vector: NDArray[np.generic]) -> NDArray[np.float64]:
    """Normaliza un vector por norma L2; los vectores nulos siguen nulos."""
    arreglo = np.asarray(vector, dtype=np.float64).ravel()
    norma = np.linalg.norm(arreglo)
    return arreglo / norma if norma > 0 else arreglo


def firma_desde_matriz(matriz: NDArray[np.generic]) -> NDArray[np.float64]:
    """Concatena los marginales por filas y columnas, ambos normalizados."""
    arreglo = np.asarray(matriz, dtype=np.float64)
    if arreglo.ndim != 2 or min(arreglo.shape) < 1:
        raise ValueError("La entrada debe ser una matriz 2D no vacía.")
    filas = normalizar(arreglo.sum(axis=1))
    columnas = normalizar(arreglo.sum(axis=0))
    # La región central concentra las variaciones lentas; las marginales
    # conservan información agregada que el recorte por sí solo pierde.
    centro_y, centro_x = np.array(arreglo.shape) // 2
    radio_y, radio_x = max(2, arreglo.shape[0] // 8), max(2, arreglo.shape[1] // 8)
    bajas = arreglo[centro_y-radio_y:centro_y+radio_y, centro_x-radio_x:centro_x+radio_x].ravel()
    return normalizar(np.concatenate((normalizar(bajas), filas, columnas)))


def firma_imagen(
    imagen: NDArray[np.generic],
    forma: tuple[int, int] = (64, 64),
    sigma: float = 0.5,
) -> NDArray[np.float64]:
    """Genera la firma de una imagen usando Fourier-Mellin analítica."""
    from .transformadas import fourier_mellin_analitica

    return firma_desde_matriz(fourier_mellin_analitica(imagen, forma, sigma))
