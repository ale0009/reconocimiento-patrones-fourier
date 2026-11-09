# Reconocimiento de patrones con Fourier-Mellin

## Problema

Clasificar letras dibujadas en imágenes con cambios de posición, orientación, escala y ruido. Las cifras de este repositorio corresponden exclusivamente a datos sintéticos generados por el código.

## Enfoque

Se resta la media de la imagen y se aplica una ventana Hann antes de calcular `|FFT2(I)|`; después `fftshift` coloca la frecuencia cero en el centro. El espectro se remuestrea bilinealmente en coordenadas log-polares, donde la rotación se vuelve un desplazamiento angular y la escala un desplazamiento radial logarítmico. La magnitud de la segunda FFT reduce la sensibilidad a esos desplazamientos.

La firma concatena el recorte central de bajas frecuencias con las sumas por filas y columnas, y normaliza el vector con norma L2. Cada clase tiene 30 referencias transformadas. Se estandariza cada dimensión con media y desviación calculadas únicamente sobre esas referencias y se clasifica por vecino más cercano euclidiano.

La semilla 42 genera referencias de entrenamiento; 31415 genera validación y 27182 genera prueba. Se eligió el número de referencias comparando alternativas solo en validación. La partición de prueba se reserva para la medición final.

## Cómo ejecutarlo

Se requiere Python 3.11 y `uv`.

```bash
uv sync --dev
uv run python -m fourier_patrones evaluar
uv run pytest -q
```

La CLI imprime las precisiones de validación y prueba, además de la matriz de confusión de prueba, que guarda en `resultados/matriz_confusion.png`.

## Resultados

Medición reproducible con `uv run python -m fourier_patrones evaluar`:

| Versión/configuración | Validación | Prueba | Aporte observado |
|---|---:|---:|---|
| Base, evaluación anterior | — | 73,75 % (59/80) | Descriptor de marginales y referencias base del proyecto. |
| Mejorada | 95,00 % (76/80) | 93,75 % (75/80) | Ventana Hann, firma con bajas frecuencias y marginales, 30 referencias por clase y estandarización usando referencias. |

En una comparación preliminar con la partición de validación, aumentar de 3 a 30 referencias por clase elevó la precisión de 83,75 % a 95,00 % con firma y estandarización mejoradas. Las cifras finales impresas por el comando son las de la tabla.

En el trabajo académico original se reportó una precisión de 95,4 % con imágenes en blanco y negro y escala de grises; es una cifra del trabajo original, no una medición de esta reimplementación.

## Limitaciones

Las formas se renderizan con una fuente disponible en el sistema; por ello, detalles de tipografía pueden variar entre equipos. El conjunto es pequeño y sintético, y no estima el desempeño en imágenes reales. La prueba solo representa una semilla fija.

## Origen

Basado en un trabajo académico en equipo de la Universidad ECCI; esta es una reimplementación individual y abierta.
