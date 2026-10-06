# Plan de pruebas

## Objetivo

Verificar que las funciones principales del Sistema de Control de Inventario operen de acuerdo con
los requisitos, que los datos se validen correctamente y que las entradas y salidas mantengan
existencias consistentes.

## Alcance

Incluye: registro, consulta, modificación y eliminación de productos; consulta de existencias;
registro de entradas y salidas; reporte básico de inventario; validación de datos y manejo de errores.

No incluye: pruebas de rendimiento, seguridad ni interfaz gráfica (el sistema se usa por línea de comandos).

## Elementos que serán probados

| Elemento | Módulo | Pruebas |
|---|---|---|
| Registro, consulta, modificación y baja de productos | `service.py`, `repository.py` | `tests/test_productos.py` |
| Existencias y movimientos (entradas y salidas) | `service.py`, `repository.py` | `tests/test_movimientos.py` |
| Validación de datos y errores | `validacion.py`, `errors.py` | `tests/test_validacion.py` |
| Reporte de inventario | `reporte.py` | `tests/test_reporte.py` |
| Persistencia y línea de comandos | `repository.py`, `cli.py` | `tests/test_integracion.py` |
| Comportamientos que no deben romperse | todos | `tests/test_regresion.py` |

## Tipos de pruebas

| Tipo | Marcador pytest | Descripción |
|---|---|---|
| Funcionales | `funcional` | Cada operación produce el resultado esperado con datos válidos |
| Integración | `integracion` | Servicio, base de datos SQLite en disco y CLI trabajan juntos |
| Validación de datos | `validacion` | Se aceptan datos correctos y se rechazan los incorrectos |
| Regresión | `regresion` | Los cambios nuevos no rompen lo que ya funcionaba |

Ejecución por tipo: `pytest -m funcional`, `pytest -m validacion`, etc.

## Criterios de aceptación

Una funcionalidad se acepta cuando:

1. Produce el resultado esperado con entradas válidas.
2. Rechaza las entradas inválidas con un mensaje claro y sin modificar los datos.
3. No genera errores no controlados.
4. Sus pruebas automatizadas pasan en la integración continua.

## Criterios de aprobación y rechazo

- **Aprobada:** el resultado obtenido coincide con el esperado y no hay errores asociados.
- **No aprobada:** el resultado difiere del esperado, ocurre un error no previsto o no se cumple algún criterio de aceptación.
- **Liberación a `main`:** todas las pruebas aprobadas y cobertura de código igual o superior a 85 %.

## Ambiente de pruebas

| Elemento | Detalle |
|---|---|
| Sistema operativo | Windows 10/11, Linux (GitHub Actions: Ubuntu) o macOS |
| Lenguaje | Python 3.11, 3.12 y 3.13 (matriz de CI) |
| Base de datos | SQLite en memoria (`:memory:`) para pruebas unitarias; archivo temporal para integración |
| Contenedor | `docker build --target test .` |
| Integración continua | GitHub Actions (`.github/workflows/tests.yml`) |

## Responsables

| Actividad | Responsable |
|---|---|
| Diseñar y mantener los casos de prueba | [Integrante 1] |
| Ejecutar las pruebas y registrar resultados | [Integrante 2] |
| Reportar incidencias en Trello | [Integrante 3] |
| Revisar correcciones y aprobar Pull Requests | [Integrante 4] |

## Herramientas utilizadas

Visual Studio Code, Python, pytest, pytest-cov, Git, GitHub, GitHub Actions, Docker y Trello.
