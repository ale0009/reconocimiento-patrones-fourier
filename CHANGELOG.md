# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-01

### Añadido
- Implementación del componente `datos`: Generación sintética de imágenes de letras, particionado reproducible (entrenamiento, validación, prueba) y renderizado tipográfico..
- Implementación del componente `transformadas`: Preprocesamiento con ventana Hann, sustracción de media, cálculo de FFT2 centrada y remuestreo log-polar bilineal..
- Implementación del componente `firmas`: Extracción del vector de firma concatenando bajas frecuencias centrales y proyecciones marginales con normalización L2..
- Implementación del componente `clasificador`: Estandarización dimensional basada en referencias de entrenamiento y asignación de clase por vecino más cercano euclidiano..
- Implementación del componente `__main__`: Punto de entrada CLI para coordinar la evaluación, reportar métricas de validación y prueba, y exportar la matriz de confusión..
- Configuración de flujo de trabajo de integración continua.
- Documentación técnica, guías de arquitectura y políticas de seguridad.
