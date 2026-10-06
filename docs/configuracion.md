# Configuración del entorno

## Herramientas

| Necesidad | Herramienta | Versión | Configuración | Propósito |
|---|---|---|---|---|
| Editor/IDE | Visual Studio Code | ___ (`code --version`) | Extensión *Python*; intérprete `.venv`; pruebas con pytest (`.vscode/settings.json`) | Desarrollo |
| Lenguaje | Python | ___ (`python --version`) | 3.11 o superior; entorno virtual `.venv` | Lógica del sistema |
| Control de versiones | Git | ___ (`git --version`) | Nombre, correo, rama inicial `main` | Historial del código |
| Repositorio remoto | GitHub | Servicio web | Repositorio `sistema-control-inventario`; ramas `main` y `develop` protegidas | Almacenamiento y revisión |
| Gestión del proyecto | Trello | Servicio web | Columnas: Pendiente, En proceso, En revisión, Terminado | Organizar tareas |
| Pruebas | pytest, pytest-cov | `pip show pytest` | `pytest.ini`: `pythonpath = src`, marcadores por tipo de prueba | Pruebas automatizadas |
| Contenedores | Docker | ___ (`docker --version`) | `Dockerfile` multietapa (`test` y `runtime`); volumen `/data` | Ambiente reproducible |
| CI/CD | GitHub Actions | Servicio web | `.github/workflows/tests.yml` | Pruebas automáticas |
| Documentación | Markdown | N/A | Carpeta `docs/` y `README.md` | Documentar el proyecto |

La columna Versión se completa con la salida del comando indicado en cada equipo.

## Configuración de Git

```bash
git config --global user.name "Nombre Apellido"
git config --global user.email "correo@ejemplo.com"
git config --global init.defaultBranch main
git config --global core.autocrlf input     # en Windows: true
git config --list
```

## Creación del repositorio y primer envío

```bash
git init -b main
git add .
git commit -m "chore: estructura inicial del proyecto"
git remote add origin https://github.com/USUARIO/sistema-control-inventario.git
git push -u origin main
git switch -c develop
git push -u origin develop
```

## Entorno de Python

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell
source .venv/bin/activate           # Linux / macOS
pip install -r requirements.txt
pytest
```

## Protección de ramas en GitHub

*Settings → Branches → Add branch ruleset* para `main` y `develop`:

- Require a pull request before merging (1 aprobación).
- Require status checks to pass: seleccionar `Pruebas (Python 3.12)` y `Imagen Docker`
  (aparecen después de la primera ejecución del workflow).

## Evidencias

| Figura | Qué mostrar |
|---|---|
| 1 | VS Code con el proyecto abierto y la extensión de Python |
| 2 | `git config --list` y `git --version` |
| 3 | Repositorio creado en GitHub |
| 4 | Tablero de Trello |
| 5 | `pytest` en la terminal con todas las pruebas aprobadas |
| 6 | `docker build --target test .` y `docker run ... reporte` |
| 7 | Workflow de GitHub Actions en verde (pestaña *Actions*) |
| 8 | Estructura final del repositorio |
