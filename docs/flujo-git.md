# Flujo de trabajo con Git

## Ramas

```text
main                      ← versión estable (protegida)
 └── develop              ← integración (protegida)
      ├── feature/productos
      ├── feature/inventario
      └── feature/reportes
```

| Rama | Uso | Quién escribe |
|---|---|---|
| `main` | Versión liberada. Cada merge recibe una etiqueta (`v1.0.0`) | Solo mediante Pull Request desde `develop` |
| `develop` | Integración del trabajo terminado | Solo mediante Pull Request desde `feature/*` |
| `feature/<nombre>` | Una funcionalidad por rama | Cada integrante |

## Paso a paso

1. **Crear el repositorio.** En GitHub: *New repository* → `sistema-control-inventario`. Localmente: `git init -b main`, primer commit y `git push -u origin main`.
2. **Crear ramas.** `git switch -c develop` y `git push -u origin develop`. Después, por cada funcionalidad: `git switch develop && git pull && git switch -c feature/productos`.
3. **Desarrollar.** Escribir código y su prueba. Ejecutar `pytest` antes de cada commit.
4. **Commit.** `git add .` y `git commit -m "feat: agrega registro de productos"`. Mensajes cortos con prefijo: `feat`, `fix`, `test`, `docs`, `chore`.
5. **Push.** `git push -u origin feature/productos`.
6. **Pull Request.** En GitHub: *Compare & pull request* con base `develop`. Se llena la plantilla `.github/pull_request_template.md`.
7. **Revisión de código.** Otro integrante revisa, comenta y aprueba. GitHub Actions debe mostrar las pruebas en verde.
8. **Integración a `develop`.** *Squash and merge* o *Merge pull request*. Después: `git switch develop && git pull`.
9. **Liberación a `main`.** Pull Request `develop` → `main`, aprobado por el equipo; luego `git tag v1.0.0 && git push --tags`.

## Evidencias que se deben capturar

- Repositorio creado.
- Ramas (`Code → branches`).
- Historial de commits (`git log --oneline --graph --all` o la pestaña *Commits*).
- Pull Request abierto, con la revisión y las pruebas en verde.
- Rama integrada (PR en estado *Merged*).
