"""Transformadas para construir un descriptor invariante a similitudes."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import map_coordinates
from scipy.signal.windows import hann

FloatArray = NDArray[np.float64]


def espectro_magnitud(imagen: NDArray[np.generic]) -> FloatArray:
    """Devuelve el espectro de magnitud 2D centrado de una imagen."""
    gris = np.asarray(imagen, dtype=np.float64)
    if gris.ndim != 2 or min(gris.shape) < 2:
        raise ValueError("La imagen debe ser una matriz 2D de al menos 2x2.")
    ventana = np.outer(hann(gris.shape[0], sym=False), hann(gris.shape[1], sym=False))
    centrada = (gris - gris.mean()) * ventana
    return np.abs(np.fft.fftshift(np.fft.fft2(centrada)))


def remuestrear_log_polar(
    espectro: NDArray[np.generic],
    forma: tuple[int, int] = (64, 64),
    sigma: float = 0.5,
) -> FloatArray:
    """Remuestrea la magnitud espectral en coordenadas log-polares.

    ``sigma`` (estrictamente positivo) amortigua las frecuencias lejanas al
    centro y evita que el borde domine el descriptor.
    """
    datos = np.asarray(espectro, dtype=np.float64)
    if datos.ndim != 2 or min(datos.shape) < 2:
        raise ValueError("El espectro debe ser una matriz 2D de al menos 2x2.")
    if len(forma) != 2 or min(forma) < 2:
        raise ValueError("forma debe contener dos dimensiones de al menos 2.")
    if sigma <= 0:
        raise ValueError("sigma debe ser mayor que cero.")

    alto, ancho = datos.shape
    centro_y, centro_x = (alto - 1) / 2, (ancho - 1) / 2
    radio_max = max(1.0, min(alto, ancho) / 2)
    radios = np.expm1(np.linspace(0, np.log1p(radio_max), forma[0]))
    angulos = np.linspace(0, 2 * np.pi, forma[1], endpoint=False)
    rr, aa = np.meshgrid(radios, angulos, indexing="ij")
    coords = np.array([centro_y + rr * np.sin(aa), centro_x + rr * np.cos(aa)])
    muestreada = map_coordinates(datos, coords, order=1, mode="constant", cval=0.0)
    amortiguacion = np.exp(-sigma * rr / radio_max)
    return np.log1p(muestreada) * amortiguacion


def fourier_mellin_analitica(
    imagen: NDArray[np.generic],
    forma: tuple[int, int] = (64, 64),
    sigma: float = 0.5,
) -> FloatArray:
    """Calcula la magnitud de la segunda FFT sobre el espectro log-polar."""
    log_polar = remuestrear_log_polar(espectro_magnitud(imagen), forma, sigma)
    return np.abs(np.fft.fftshift(np.fft.fft2(log_polar)))
