"""Clasificación de firmas mediante vecino más cercano."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def distancia(a: NDArray[np.generic], b: NDArray[np.generic], metrica: str = "euclidiana") -> float:
    """Calcula distancia euclidiana o distancia basada en correlación."""
    x, y = np.asarray(a, dtype=float).ravel(), np.asarray(b, dtype=float).ravel()
    if x.shape != y.shape:
        raise ValueError("Las firmas deben tener la misma forma.")
    if metrica == "euclidiana":
        return float(np.linalg.norm(x - y))
    if metrica == "correlacion":
        x0, y0 = x - x.mean(), y - y.mean()
        denominador = np.linalg.norm(x0) * np.linalg.norm(y0)
        return float(1 - np.dot(x0, y0) / denominador) if denominador else 1.0
    raise ValueError("metrica debe ser 'euclidiana' o 'correlacion'.")


def predecir(
    referencias: NDArray[np.generic],
    etiquetas: NDArray[np.generic],
    consulta: NDArray[np.generic],
    metrica: str = "euclidiana",
) -> str:
    """Retorna la clase de la referencia más cercana."""
    firmas = np.asarray(referencias, dtype=float)
    clases = np.asarray(etiquetas)
    if firmas.ndim != 2 or len(firmas) != len(clases) or len(clases) == 0:
        raise ValueError("Se requieren referencias 2D y una etiqueta por fila.")
    distancias = [distancia(firma, consulta, metrica) for firma in firmas]
    return str(clases[int(np.argmin(distancias))])
