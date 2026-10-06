"""Reporte básico de inventario."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .models import Producto


@dataclass(frozen=True)
class Reporte:
    """Resumen del inventario en un momento dado."""

    productos: tuple[Producto, ...]

    @property
    def total_productos(self) -> int:
        return len(self.productos)

    @property
    def total_unidades(self) -> int:
        return sum(p.existencia for p in self.productos)

    @property
    def valor_total(self) -> Decimal:
        return sum((p.valor_total for p in self.productos), Decimal("0.00"))

    @property
    def sin_existencia(self) -> tuple[str, ...]:
        return tuple(p.codigo for p in self.productos if p.existencia == 0)

    def a_texto(self) -> str:
        """Devuelve el reporte como tabla de texto para imprimir en terminal."""
        encabezado = f"{'CÓDIGO':<12}{'NOMBRE':<30}{'PRECIO':>10}{'EXIST.':>8}{'VALOR':>12}"
        lineas = ["REPORTE DE INVENTARIO", "=" * len(encabezado), encabezado, "-" * len(encabezado)]
        for p in self.productos:
            lineas.append(
                f"{p.codigo:<12}{p.nombre[:28]:<30}{p.precio:>10.2f}"
                f"{p.existencia:>8}{p.valor_total:>12.2f}"
            )
        if not self.productos:
            lineas.append("(No hay productos registrados)")
        lineas += [
            "-" * len(encabezado),
            f"Productos registrados : {self.total_productos}",
            f"Unidades en existencia: {self.total_unidades}",
            f"Valor total           : {self.valor_total:.2f}",
        ]
        if self.sin_existencia:
            lineas.append("Sin existencia        : " + ", ".join(self.sin_existencia))
        return "\n".join(lineas)
