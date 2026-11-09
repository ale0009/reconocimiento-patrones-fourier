"""Generación reproducible de formas y ejemplos transformados."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import rotate, shift, zoom

CLASES = ("A", "B", "C", "D", "E", "F", "H", "L", "P", "R")


@dataclass(frozen=True)
class Conjunto:
    """Imágenes, etiquetas y partición reproducible de referencias/consultas."""

    referencias: NDArray[np.float64]
    etiquetas_referencia: NDArray[np.str_]
    consultas: NDArray[np.float64]
    etiquetas_consulta: NDArray[np.str_]


def _fuente() -> ImageFont.ImageFont:
    """Busca una fuente instalada y usa la tipografía Pillow como respaldo."""
    for ruta in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(ruta, 54)
        except OSError:
            continue
    return ImageFont.load_default()


def imagen_base(clase: str, tamano: int = 64) -> NDArray[np.float64]:
    """Dibuja una letra o forma binaria centrada en una imagen en gris."""
    if clase not in CLASES:
        raise ValueError(f"Clase desconocida: {clase}")
    lienzo = Image.new("L", (tamano, tamano), 0)
    dibujo = ImageDraw.Draw(lienzo)
    caja = dibujo.textbbox((0, 0), clase, font=_fuente(), stroke_width=1)
    x = (tamano - (caja[2] - caja[0])) / 2 - caja[0]
    y = (tamano - (caja[3] - caja[1])) / 2 - caja[1]
    dibujo.text((x, y), clase, fill=255, font=_fuente(), stroke_width=1)
    return np.asarray(lienzo, dtype=np.float64) / 255.0


def transformar(
    imagen: NDArray[np.generic], rng: np.random.Generator, ruido: float = 0.035
) -> NDArray[np.float64]:
    """Aplica escala, rotación, traslación y ruido con borde constante."""
    escala = float(rng.uniform(0.6, 1.4))
    girada = rotate(np.asarray(imagen), float(rng.uniform(0, 360)), reshape=False, order=1, mode="constant")
    escalada = zoom(girada, escala, order=1, mode="constant")
    alto, ancho = escalada.shape
    salida = np.zeros_like(imagen, dtype=float)
    y0, x0 = max(0, (alto - salida.shape[0]) // 2), max(0, (ancho - salida.shape[1]) // 2)
    recorte = escalada[y0 : y0 + min(alto, salida.shape[0]), x0 : x0 + min(ancho, salida.shape[1])]
    dy, dx = (salida.shape[0] - recorte.shape[0]) // 2, (salida.shape[1] - recorte.shape[1]) // 2
    salida[dy : dy + recorte.shape[0], dx : dx + recorte.shape[1]] = recorte
    desplazada = shift(salida, (float(rng.integers(-8, 9)), float(rng.integers(-8, 9))), order=1, mode="constant")
    return np.clip(desplazada + rng.normal(0, ruido, desplazada.shape), 0, 1)


def generar_dataset(
    semilla: int = 42, referencias_por_clase: int = 3, consultas_por_clase: int = 8
) -> Conjunto:
    """Genera un dataset sintético fijo; referencias base y consultas aleatorias."""
    if referencias_por_clase < 1 or consultas_por_clase < 1:
        raise ValueError("Debe haber al menos una referencia y una consulta por clase.")
    rng = np.random.default_rng(semilla)
    refs, etiquetas_ref, consultas, etiquetas_consulta = [], [], [], []
    for clase in CLASES:
        base = imagen_base(clase)
        for indice in range(referencias_por_clase):
            refs.append(base if indice == 0 else transformar(base, rng, ruido=0.01))
            etiquetas_ref.append(clase)
        for _ in range(consultas_por_clase):
            consultas.append(transformar(base, rng))
            etiquetas_consulta.append(clase)
    return Conjunto(
        np.asarray(refs), np.asarray(etiquetas_ref), np.asarray(consultas), np.asarray(etiquetas_consulta)
    )
