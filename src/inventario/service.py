"""Lógica de negocio del Sistema de Control de Inventario."""

from __future__ import annotations

from datetime import datetime, timezone

from . import validacion as v
from .errors import ProductoNoEncontradoError
from .models import ENTRADA, SALIDA, Movimiento, Producto
from .repository import RepositorioSQLite
from .reporte import Reporte


class InventarioService:
    """Operaciones del inventario: productos, existencias y reportes."""

    def __init__(self, repositorio: RepositorioSQLite) -> None:
        self._repo = repositorio

    # ------------------------------------------------------------- productos
    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        precio: object,
        existencia: object = 0,
        descripcion: str = "",
    ) -> Producto:
        producto = Producto(
            codigo=v.validar_codigo(codigo),
            nombre=v.validar_nombre(nombre),
            precio=v.validar_precio(precio),
            existencia=v.validar_existencia(existencia),
            descripcion=v.validar_descripcion(descripcion),
        )
        self._repo.agregar(producto)
        return producto

    def consultar_producto(self, codigo: str) -> Producto:
        codigo = v.validar_codigo(codigo)
        producto = self._repo.obtener(codigo)
        if producto is None:
            raise ProductoNoEncontradoError(codigo)
        return producto

    def listar_productos(self) -> list[Producto]:
        return self._repo.listar()

    def modificar_producto(
        self,
        codigo: str,
        *,
        nombre: str | None = None,
        precio: object = None,
        descripcion: str | None = None,
    ) -> Producto:
        """Modifica nombre, precio o descripción. La existencia solo cambia
        con entradas y salidas, para conservar el historial consistente."""
        actual = self.consultar_producto(codigo)
        nuevo = Producto(
            codigo=actual.codigo,
            nombre=actual.nombre if nombre is None else v.validar_nombre(nombre),
            precio=actual.precio if precio is None else v.validar_precio(precio),
            existencia=actual.existencia,
            descripcion=(
                actual.descripcion
                if descripcion is None
                else v.validar_descripcion(descripcion)
            ),
        )
        self._repo.actualizar(nuevo)
        return nuevo

    def eliminar_producto(self, codigo: str) -> None:
        codigo = v.validar_codigo(codigo)
        if not self._repo.eliminar(codigo):
            raise ProductoNoEncontradoError(codigo)

    # ----------------------------------------------------------- existencias
    def consultar_existencia(self, codigo: str) -> int:
        return self.consultar_producto(codigo).existencia

    def registrar_entrada(self, codigo: str, cantidad: object, motivo: str = "") -> Producto:
        return self._mover(codigo, ENTRADA, cantidad, motivo)

    def registrar_salida(self, codigo: str, cantidad: object, motivo: str = "") -> Producto:
        return self._mover(codigo, SALIDA, cantidad, motivo)

    def _mover(self, codigo: str, tipo: str, cantidad: object, motivo: str) -> Producto:
        producto = self.consultar_producto(codigo)
        movimiento = Movimiento(
            codigo=producto.codigo,
            tipo=tipo,
            cantidad=v.validar_cantidad(cantidad),
            fecha=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            motivo=v.validar_descripcion(motivo),
        )
        self._repo.aplicar_movimiento(movimiento)
        return self.consultar_producto(producto.codigo)

    def historial(self, codigo: str | None = None) -> list[Movimiento]:
        if codigo is not None:
            codigo = self.consultar_producto(codigo).codigo
        return self._repo.movimientos(codigo)

    # --------------------------------------------------------------- reporte
    def generar_reporte(self) -> Reporte:
        return Reporte(productos=tuple(self._repo.listar()))
