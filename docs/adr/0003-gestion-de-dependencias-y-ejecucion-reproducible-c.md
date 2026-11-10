# ADR-0003: Gestión de dependencias y ejecución reproducible con uv y hatchling

- **Estado:** Aceptado
- **Fecha:** 2026-11-09
- **Proyecto:** Reconocimiento de patrones con Fourier-Mellin

## Contexto

Se necesita un entorno determinista con Python 3.11 sin sobrecarga de configuración.

## Decisión

Configurar empaquetado estándar PEP 621 con backend hatchling y bloqueo de dependencias en uv.lock.

## Consecuencias

Garantiza ejecuciones de prueba y benchmarking completamente reproducibles mediante uv run.
