"""CP-13: reporte básico de inventario."""

from decimal import Decimal

import pytest

pytestmark = pytest.mark.funcional


def test_cp13_reporte_despues_de_registrar_movimientos(servicio):
    servicio.registrar_producto("A1", "Mouse", "100", 10)
    servicio.registrar_producto("B2", "Teclado", "250.50", 4)
    servicio.registrar_producto("C3", "Monitor", "1500", 0)
    servicio.registrar_entrada("A1", 5)
    servicio.registrar_salida("B2", 4)

    reporte = servicio.generar_reporte()

    assert reporte.total_productos == 3
    assert reporte.total_unidades == 15  # 15 + 0 + 0
    assert reporte.valor_total == Decimal("1500.00")  # 15 x 100
    assert reporte.sin_existencia == ("B2", "C3")


def test_reporte_en_texto_incluye_productos_y_totales(con_producto):
    texto = con_producto.generar_reporte().a_texto()

    assert "REPORTE DE INVENTARIO" in texto
    assert "P001" in texto and "Teclado USB" in texto
    assert "Valor total           : 1000.00" in texto


def test_reporte_de_inventario_vacio(servicio):
    reporte = servicio.generar_reporte()

    assert reporte.total_productos == 0
    assert reporte.valor_total == Decimal("0.00")
    assert "No hay productos registrados" in reporte.a_texto()
