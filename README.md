# Sistema de Control de Inventario

![Tests](https://github.com/USUARIO/sistema-control-inventario/actions/workflows/tests.yml/badge.svg)

Aplicación de línea de comandos en Python para controlar el inventario de una empresa:

- Registrar, consultar, modificar y eliminar productos.
- Consultar existencias.
- Registrar entradas y salidas de mercancía (con historial).
- Generar un reporte básico de inventario.

> Reemplaza `USUARIO` en la insignia de arriba por tu usuario u organización de GitHub.

## Estructura del repositorio

```text
sistema-control-inventario/
├── src/inventario/        Código fuente (modelo, validación, repositorio, servicio, CLI)
├── tests/                 Pruebas automatizadas con pytest
├── docs/                  Documentación del proyecto
│   ├── configuracion.md
│   ├── plan-pruebas.md
│   ├── casos-prueba.md
│   ├── despliegue.md
│   └── flujo-git.md
├── .github/
│   ├── workflows/tests.yml        Integración continua (GitHub Actions)
│   └── pull_request_template.md
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
```

## Requisitos

- Python 3.11 o superior
- Git
- Docker (opcional)

## Instalación

Windows (PowerShell):

```powershell
git clone https://github.com/USUARIO/sistema-control-inventario.git
cd sistema-control-inventario
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux / macOS:

```bash
git clone https://github.com/USUARIO/sistema-control-inventario.git
cd sistema-control-inventario
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

Todos los comandos se ejecutan desde la raíz del repositorio. La primera vez, define
`PYTHONPATH` para que Python encuentre el paquete (en `pytest` ya está configurado):

```bash
export PYTHONPATH=src            # Windows PowerShell: $env:PYTHONPATH = "src"
python -m inventario registrar P001 "Mouse USB" 150.50 --existencia 10 --descripcion "Inalámbrico"
python -m inventario consultar P001
python -m inventario listar
python -m inventario modificar P001 --precio 175
python -m inventario entrada P001 5 --motivo "Compra a proveedor"
python -m inventario salida P001 3 --motivo "Venta"
python -m inventario existencia P001
python -m inventario historial P001
python -m inventario reporte
python -m inventario eliminar P001
```

Los datos se guardan en `inventario.db` (SQLite). Para usar otro archivo:
`--db ruta/archivo.db` o la variable de entorno `INVENTARIO_DB`.

Reglas de validación: el código admite letras, números, `-` y `_` (máximo 20) y no distingue
mayúsculas; el precio debe ser mayor o igual a 0; la existencia inicial, entera y mayor o igual a 0;
las cantidades de entrada y salida, enteras y mayores que 0; no se permite una salida mayor que la
existencia.

## Pruebas

```bash
pytest                                   # todas las pruebas
pytest --cov=inventario --cov-report=term-missing
pytest -m funcional                      # también: validacion, integracion, regresion
```

## Docker

```bash
docker build --target test .             # corre las pruebas dentro de un contenedor
docker build -t inventario .             # imagen final (sin pytest)
docker run --rm -v inventario-datos:/data inventario registrar P001 "Mouse USB" 150.50 --existencia 10
docker run --rm -v inventario-datos:/data inventario reporte
```

El volumen `inventario-datos` conserva la base de datos entre ejecuciones.

## Integración continua

El workflow `.github/workflows/tests.yml` se ejecuta en cada `push` y `pull_request` hacia
`main` y `develop`: corre las pruebas en Python 3.11, 3.12 y 3.13 (con cobertura mínima de 85 %)
y construye la imagen Docker con una prueba de humo.

## Flujo de trabajo en Git

`main` (estable) ← `develop` (integración) ← `feature/nombre` (trabajo de cada integrante).
Detalle en [docs/flujo-git.md](docs/flujo-git.md).
* Módulo de gestión de productos.
