"""Modelos de datos del inventario."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

ENTRADA = "ENTRADA"
SALIDA = "SALIDA"


@dataclass(frozen=True)
class Producto:
    """Un producto del catálogo con su existencia actual."""

    codigo: str
    nombre: str
    precio: Decimal
    existencia: int = 0
    descripcion: str = ""

    @property
    def valor_total(self) -> Decimal:
        """Valor del inventario de este producto (precio x existencia)."""
        return self.precio * self.existencia


@dataclass(frozen=True)
class Movimiento:
    """Una entrada o salida de mercancía."""

    codigo: str
    tipo: str
    cantidad: int
    fecha: str
    motivo: str = ""
    id: int | None = None
