"""Interfaz de línea de comandos del inventario.

Ejemplos:
    python -m inventario registrar P001 "Mouse USB" 150.50 --existencia 10
    python -m inventario entrada P001 5
    python -m inventario reporte
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Sequence, TextIO

from .errors import InventarioError
from .models import Producto
from .repository import RepositorioSQLite
from .service import InventarioService

DB_POR_DEFECTO = "inventario.db"


def _construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="inventario", description="Sistema de Control de Inventario"
    )
    parser.add_argument(
        "--db",
        default=os.environ.get("INVENTARIO_DB", DB_POR_DEFECTO),
        help="Ruta de la base de datos SQLite (o variable INVENTARIO_DB).",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    p = sub.add_parser("registrar", help="Registrar un producto nuevo")
    p.add_argument("codigo")
    p.add_argument("nombre")
    p.add_argument("precio")
    p.add_argument("--existencia", default="0", help="Existencia inicial (por defecto 0)")
    p.add_argument("--descripcion", default="")

    p = sub.add_parser("consultar", help="Consultar un producto por código")
    p.add_argument("codigo")

    sub.add_parser("listar", help="Listar todos los productos")

    p = sub.add_parser("modificar", help="Modificar nombre, precio o descripción")
    p.add_argument("codigo")
    p.add_argument("--nombre")
    p.add_argument("--precio")
    p.add_argument("--descripcion")

    p = sub.add_parser("eliminar", help="Eliminar un producto")
    p.add_argument("codigo")

    p = sub.add_parser("existencia", help="Consultar la existencia de un producto")
    p.add_argument("codigo")

    for nombre, ayuda in (("entrada", "Registrar entrada"), ("salida", "Registrar salida")):
        p = sub.add_parser(nombre, help=f"{ayuda} de producto")
        p.add_argument("codigo")
        p.add_argument("cantidad")
        p.add_argument("--motivo", default="")

    p = sub.add_parser("historial", help="Ver movimientos de entradas y salidas")
    p.add_argument("codigo", nargs="?")

    sub.add_parser("reporte", help="Generar el reporte básico de inventario")
    return parser


def _linea(p: Producto) -> str:
    return (
        f"{p.codigo} | {p.nombre} | precio: {p.precio:.2f} | existencia: {p.existencia}"
        + (f" | {p.descripcion}" if p.descripcion else "")
    )


def _ejecutar(args: argparse.Namespace, servicio: InventarioService, out: TextIO) -> None:
    c = args.comando
    if c == "registrar":
        p = servicio.registrar_producto(
            args.codigo, args.nombre, args.precio, args.existencia, args.descripcion
        )
        print(f"Producto registrado: {_linea(p)}", file=out)
    elif c == "consultar":
        print(_linea(servicio.consultar_producto(args.codigo)), file=out)
    elif c == "listar":
        productos = servicio.listar_productos()
        if not productos:
            print("No hay productos registrados.", file=out)
        for p in productos:
            print(_linea(p), file=out)
    elif c == "modificar":
        p = servicio.modificar_producto(
            args.codigo,
            nombre=args.nombre,
            precio=args.precio,
            descripcion=args.descripcion,
        )
        print(f"Producto actualizado: {_linea(p)}", file=out)
    elif c == "eliminar":
        servicio.eliminar_producto(args.codigo)
        print(f"Producto eliminado: {args.codigo.strip().upper()}", file=out)
    elif c == "existencia":
        p = servicio.consultar_producto(args.codigo)
        print(f"Existencia de {p.codigo}: {p.existencia}", file=out)
    elif c in ("entrada", "salida"):
        registrar = servicio.registrar_entrada if c == "entrada" else servicio.registrar_salida
        p = registrar(args.codigo, args.cantidad, args.motivo)
        print(f"{c.capitalize()} registrada. Existencia de {p.codigo}: {p.existencia}", file=out)
    elif c == "historial":
        movimientos = servicio.historial(args.codigo)
        if not movimientos:
            print("Sin movimientos.", file=out)
        for m in movimientos:
            print(f"{m.fecha} | {m.codigo} | {m.tipo} | {m.cantidad} | {m.motivo}", file=out)
    elif c == "reporte":
        print(servicio.generar_reporte().a_texto(), file=out)


def main(argv: Sequence[str] | None = None, out: TextIO | None = None) -> int:
    """Punto de entrada. Devuelve 0 si todo salió bien y 1 si hubo un error controlado."""
    out = out or sys.stdout
    args = _construir_parser().parse_args(argv)
    repositorio = RepositorioSQLite(args.db)
    try:
        _ejecutar(args, InventarioService(repositorio), out)
        return 0
    except InventarioError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    finally:
        repositorio.cerrar()
