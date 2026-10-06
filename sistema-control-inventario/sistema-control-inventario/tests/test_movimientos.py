"""CP-07 y CP-08, y la consulta de existencias."""

import pytest

from inventario import ProductoNoEncontradoError

pytestmark = pytest.mark.funcional


def test_consultar_existencias(con_producto):
    assert con_producto.consultar_existencia("P001") == 10


def test_cp07_entrada_con_cantidad_valida_incrementa_existencia(con_producto):
    producto = con_producto.registrar_entrada("P001", 5, "Compra a proveedor")

    assert producto.existencia == 15
    assert con_producto.consultar_existencia("P001") == 15


def test_cp08_salida_con_cantidad_disponible_reduce_existencia(con_producto):
    producto = con_producto.registrar_salida("P001", 4, "Venta")

    assert producto.existencia == 6
    assert con_producto.consultar_existencia("P001") == 6


def test_los_movimientos_quedan_en_el_historial(con_producto):
    con_producto.registrar_entrada("P001", 5, "Compra")
    con_producto.registrar_salida("P001", 2, "Venta")

    historial = con_producto.historial("P001")

    assert [(m.tipo, m.cantidad, m.motivo) for m in historial] == [
        ("ENTRADA", 5, "Compra"),
        ("SALIDA", 2, "Venta"),
    ]


def test_movimiento_de_producto_inexistente(servicio):
    with pytest.raises(ProductoNoEncontradoError):
        servicio.registrar_entrada("P404", 1)
    with pytest.raises(ProductoNoEncontradoError):
        servicio.registrar_salida("P404", 1)
