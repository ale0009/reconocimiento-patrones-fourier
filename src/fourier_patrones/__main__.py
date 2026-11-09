"""Interfaz de línea de comandos del proyecto."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .clasificador import predecir
from .datos import generar_dataset
from .firmas import firma_imagen


def evaluar() -> None:
    """Mide validación y prueba independientes; hiperparámetros fijados antes."""
    entrenamiento = generar_dataset(semilla=42, referencias_por_clase=30, consultas_por_clase=1)
    validacion = generar_dataset(semilla=31415, referencias_por_clase=1, consultas_por_clase=8)
    prueba = generar_dataset(semilla=27182, referencias_por_clase=1, consultas_por_clase=8)
    firmas_ref = np.asarray([firma_imagen(imagen) for imagen in entrenamiento.referencias])
    media, escala = firmas_ref.mean(axis=0), firmas_ref.std(axis=0)
    escala[escala < 1e-8] = 1.0
    firmas_ref = (firmas_ref - media) / escala
    def medir(conjunto):
        firmas = [(firma_imagen(imagen) - media) / escala for imagen in conjunto.consultas]
        pred = [predecir(firmas_ref, entrenamiento.etiquetas_referencia, firma) for firma in firmas]
        return float(np.mean(conjunto.etiquetas_consulta == pred)), pred
    precision_val, _ = medir(validacion)
    precision, predicciones = medir(prueba)
    conjunto = prueba
    clases = sorted(set(conjunto.etiquetas_referencia))
    indices = {clase: indice for indice, clase in enumerate(clases)}
    matriz = np.zeros((len(clases), len(clases)), dtype=int)
    for real, predicha in zip(conjunto.etiquetas_consulta, predicciones, strict=True):
        matriz[indices[str(real)], indices[predicha]] += 1
    precision = float(np.mean(conjunto.etiquetas_consulta == predicciones))
    print(f"Validación: {precision_val * 100:.2f} % ({int(precision_val * len(validacion.consultas))}/{len(validacion.consultas)})")
    print(f"Prueba: {precision * 100:.2f} % ({int(precision * len(prueba.consultas))}/{len(prueba.consultas)})")
    print("Matriz de confusión (filas=real, columnas=predicción):")
    print("     " + " ".join(f"{clase:>3}" for clase in clases))
    for clase, fila in zip(clases, matriz, strict=True):
        print(f"{clase:>3}  " + " ".join(f"{valor:3d}" for valor in fila))

    ruta = Path("resultados/matriz_confusion.png")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    figura, eje = plt.subplots(figsize=(8, 7))
    imagen = eje.imshow(matriz, cmap="Blues")
    eje.set(xticks=range(len(clases)), yticks=range(len(clases)), xticklabels=clases,
            yticklabels=clases, xlabel="Predicción", ylabel="Clase real", title="Matriz de confusión")
    figura.colorbar(imagen, ax=eje)
    for (fila, columna), valor in np.ndenumerate(matriz):
        eje.text(columna, fila, str(valor), ha="center", va="center", color="black")
    figura.tight_layout()
    figura.savefig(ruta, dpi=150)
    plt.close(figura)
    print(f"Matriz guardada en: {ruta}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="fourier_patrones")
    subparsers = parser.add_subparsers(dest="comando", required=True)
    subparsers.add_parser("evaluar", help="Evalúa el dataset sintético reproducible")
    argumentos = parser.parse_args()
    if argumentos.comando == "evaluar":
        evaluar()


if __name__ == "__main__":
    main()
