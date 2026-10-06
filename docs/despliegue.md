# Estrategia de despliegue

## Estrategia seleccionada: despliegue continuo con contenedores (rolling) con aprobación manual a producción

El sistema es una aplicación pequeña, sin usuarios concurrentes que justifiquen mantener dos
versiones activas (Blue/Green) ni un porcentaje de tráfico (Canary). La estrategia más adecuada es
construir una imagen Docker en cada cambio integrado, validarla automáticamente y reemplazar la
versión en ejecución por la nueva.

| Elemento | Descripción |
|---|---|
| Estrategia seleccionada | Rolling / Continuous Deployment con imagen Docker |
| Ambiente | Desarrollo (equipo del integrante, rama `feature/*`) → Pruebas (GitHub Actions, rama `develop`) → Producción (imagen construida desde `main`) |
| Proceso | 1. Se integra el Pull Request a `develop`. 2. GitHub Actions ejecuta pruebas en Python 3.11–3.13. 3. Se construye la imagen (`docker build --target test .` y después la imagen final). 4. Se corre la prueba de humo en el contenedor. 5. Se hace el Pull Request `develop` → `main` con aprobación del equipo. 6. Se publica una etiqueta de versión (`v1.0.0`) y se ejecuta el contenedor nuevo con el mismo volumen `/data`. |
| Riesgos | Una versión con errores llega a producción; pérdida de datos si el volumen se borra; una migración de la base de datos incompatible |
| Ventajas | Mismo ambiente en todas partes; pruebas automáticas antes de cada liberación; despliegue repetible con un solo comando; imagen final pequeña y sin dependencias de prueba |
| Plan de recuperación | Volver a ejecutar la imagen de la etiqueta anterior (`docker run ... inventario:v0.9.0`); respaldar el volumen antes de cada despliegue; los datos viven en el volumen, no en la imagen |

## Comandos

```bash
# Construir y probar
docker build --target test .
docker build -t inventario:v1.0.0 .

# Respaldar la base de datos antes de desplegar
docker run --rm -v inventario-datos:/data -v "$PWD":/respaldo alpine \
    cp /data/inventario.db /respaldo/inventario-$(date +%F).db

# Ejecutar la versión nueva
docker run --rm -v inventario-datos:/data inventario:v1.0.0 reporte

# Recuperación: volver a la versión anterior
docker run --rm -v inventario-datos:/data inventario:v0.9.0 reporte
```

## Evolución

Si el sistema pasa a ser un servicio web con muchos usuarios, la estrategia puede cambiar a
Blue/Green o Canary, y los *feature flags* permitirían liberar funciones de forma gradual.
