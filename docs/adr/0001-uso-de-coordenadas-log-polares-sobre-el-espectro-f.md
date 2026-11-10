# ADR-0001: Uso de coordenadas log-polares sobre el espectro Fourier

- **Estado:** Aceptado
- **Fecha:** 2026-11-09
- **Proyecto:** Reconocimiento de patrones con Fourier-Mellin

## Contexto

Se requiere desacoplar y hacer invariante la clasificación frente a cambios simultáneos de escala y rotación.

## Decisión

Remuestrear bilinealmente la magnitud de la FFT2 centrada en coordenadas log-polares antes de aplicar una segunda FFT.

## Consecuencias

Convierte la rotación en desplazamiento angular y la escala en desplazamiento radial logarítmico, facilitando la extracción de firmas estables.
