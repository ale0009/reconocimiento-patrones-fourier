# ADR-0002: Ventana Hann, firma de frecuencias bajas y aumento a 30 referencias

- **Estado:** Aceptado
- **Fecha:** 2026-11-09
- **Proyecto:** Reconocimiento de patrones con Fourier-Mellin

## Contexto

La versión base alcanzaba únicamente 73,75 % de exactitud debido a efectos de borde y baja representatividad de referencias.

## Decisión

Aplicar ventana Hann previa a la FFT, concatenar bajas frecuencias con sumas marginales, normalizar en L2 y elevar referencias a 30 por clase.

## Consecuencias

Elevó la exactitud de prueba a 93,75 %, estandarizando las características exclusivamente con media y desviación de las referencias.
