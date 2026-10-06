"""Persistencia en SQLite (módulo ``sqlite3`` de la biblioteca estándar)."""

from __future__ import annotations

import sqlite3
from decimal import Decimal

from .errors import ExistenciaInsuficienteError, ProductoDuplicadoError
from .models import Movimiento, Producto

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS productos (
    codigo       TEXT PRIMARY KEY,
    nombre       TEXT NOT NULL,
    descripcion  TEXT NOT NULL DEFAULT '',
    precio       TEXT NOT NULL,
    existencia   INTEGER NOT NULL DEFAULT 0 CHECK (existencia >= 0)
);
CREATE TABLE IF NOT EXISTS movimientos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo    TEXT NOT NULL,
    tipo      TEXT NOT NULL CHECK (tipo IN ('ENTRADA', 'SALIDA')),
    cantidad  INTEGER NOT NULL CHECK (cantidad > 0),
    fecha     TEXT NOT NULL,
    motivo    TEXT NOT NULL DEFAULT ''
);
"""


def _a_producto(fila: sqlite3.Row) -> Producto:
    return Producto(
        codigo=fila["codigo"],
        nombre=fila["nombre"],
        descripcion=fila["descripcion"],
        precio=Decimal(fila["precio"]),
        existencia=fila["existencia"],
    )


class RepositorioSQLite:
    """Guarda productos y movimientos. Usar ``":memory:"`` para pruebas."""

    def __init__(self, ruta: str = ":memory:") -> None:
        self._con = sqlite3.connect(ruta)
        self._con.row_factory = sqlite3.Row
        self._con.executescript(_ESQUEMA)

    def cerrar(self) -> None:
        self._con.close()

    # ------------------------------------------------------------ productos
    def agregar(self, producto: Producto) -> None:
        try:
            with self._con:
                self._con.execute(
                    "INSERT INTO productos (codigo, nombre, descripcion, precio, existencia)"
                    " VALUES (?, ?, ?, ?, ?)",
                    (
                        producto.codigo,
                        producto.nombre,
                        producto.descripcion,
                        str(producto.precio),
                        producto.existencia,
                    ),
                )
        except sqlite3.IntegrityError:
            raise ProductoDuplicadoError(producto.codigo) from None

    def obtener(self, codigo: str) -> Producto | None:
        fila = self._con.execute(
            "SELECT * FROM productos WHERE codigo = ?", (codigo,)
        ).fetchone()
        return _a_producto(fila) if fila else None

    def listar(self) -> list[Producto]:
        filas = self._con.execute("SELECT * FROM productos ORDER BY codigo").fetchall()
        return [_a_producto(f) for f in filas]

    def actualizar(self, producto: Producto) -> None:
        """Actualiza nombre, descripción y precio (la existencia solo cambia
        mediante movimientos)."""
        with self._con:
            self._con.execute(
                "UPDATE productos SET nombre = ?, descripcion = ?, precio = ?"
                " WHERE codigo = ?",
                (
                    producto.nombre,
                    producto.descripcion,
                    str(producto.precio),
                    producto.codigo,
                ),
            )

    def eliminar(self, codigo: str) -> bool:
        with self._con:
            cursor = self._con.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
        return cursor.rowcount > 0

    # ---------------------------------------------------------- movimientos
    def aplicar_movimiento(self, movimiento: Movimiento) -> None:
        """Ajusta la existencia y guarda el movimiento en una sola transacción."""
        delta = movimiento.cantidad if movimiento.tipo == "ENTRADA" else -movimiento.cantidad
        with self._con:
            cursor = self._con.execute(
                "UPDATE productos SET existencia = existencia + ?"
                " WHERE codigo = ? AND existencia + ? >= 0",
                (delta, movimiento.codigo, delta),
            )
            if cursor.rowcount == 0:
                fila = self._con.execute(
                    "SELECT existencia FROM productos WHERE codigo = ?",
                    (movimiento.codigo,),
                ).fetchone()
                disponible = fila["existencia"] if fila else 0
                raise ExistenciaInsuficienteError(
                    movimiento.codigo, disponible, movimiento.cantidad
                )
            self._con.execute(
                "INSERT INTO movimientos (codigo, tipo, cantidad, fecha, motivo)"
                " VALUES (?, ?, ?, ?, ?)",
                (
                    movimiento.codigo,
                    movimiento.tipo,
                    movimiento.cantidad,
                    movimiento.fecha,
                    movimiento.motivo,
                ),
            )

    def movimientos(self, codigo: str | None = None) -> list[Movimiento]:
        consulta = "SELECT * FROM movimientos"
        parametros: tuple[str, ...] = ()
        if codigo is not None:
            consulta += " WHERE codigo = ?"
            parametros = (codigo,)
        consulta += " ORDER BY id"
        return [
            Movimiento(
                id=f["id"],
                codigo=f["codigo"],
                tipo=f["tipo"],
                cantidad=f["cantidad"],
                fecha=f["fecha"],
                motivo=f["motivo"],
            )
            for f in self._con.execute(consulta, parametros).fetchall()
        ]
