"""CP-01 a CP-06: alta, consulta, modificación y baja de productos."""

from decimal import Decimal

import pytest

from inventario import ProductoDuplicadoError, ProductoNoEncontradoError

pytestmark = pytest.mark.funcional


def test_cp01_registrar_producto_con_datos_validos(servicio):
    producto = servicio.registrar_producto("P001", "Mouse USB", "150.50", 5)

    assert producto.codigo == "P001"
    assert producto.precio == Decimal("150.50")
    assert servicio.consultar_producto("P001").existencia == 5


def test_cp02_registrar_producto_con_codigo_duplicado(con_producto):
    with pytest.raises(ProductoDuplicadoError, match="P001"):
        con_producto.registrar_producto("P001", "Otro nombre", "10")

    assert len(con_producto.listar_productos()) == 1
    assert con_producto.consultar_producto("P001").nombre == "Teclado USB"


def test_cp03_consultar_producto_con_codigo_existente(con_producto):
    producto = con_producto.consultar_producto("P001")

    assert producto.nombre == "Teclado USB"
    assert producto.existencia == 10


def test_cp04_consultar_producto_con_codigo_inexistente(servicio):
    with pytest.raises(ProductoNoEncontradoError, match="NO-EXISTE"):
        servicio.consultar_producto("NO-EXISTE")


def test_cp05_modificar_producto_con_datos_validos(con_producto):
    actualizado = con_producto.modificar_producto("P001", nombre="Teclado Gamer", precio="250")

    assert actualizado.nombre == "Teclado Gamer"
    assert actualizado.precio == Decimal("250.00")
    # Lo que no se modificó se conserva.
    assert actualizado.descripcion == "Teclado español"
    assert con_producto.consultar_producto("P001") == actualizado


def test_cp06_eliminar_producto_existente(con_producto):
    con_producto.eliminar_producto("P001")

    with pytest.raises(ProductoNoEncontradoError):
        con_producto.consultar_producto("P001")
    assert con_producto.listar_productos() == []


def test_modificar_producto_inexistente(servicio):
    with pytest.raises(ProductoNoEncontradoError):
        servicio.modificar_producto("P404", nombre="X")


def test_eliminar_producto_inexistente(servicio):
    with pytest.raises(ProductoNoEncontradoError):
        servicio.eliminar_producto("P404")


def test_el_codigo_no_distingue_mayusculas(servicio):
    servicio.registrar_producto("abc-1", "Cable", "20")

    assert servicio.consultar_producto("ABC-1").codigo == "ABC-1"
    with pytest.raises(ProductoDuplicadoError):
        servicio.registrar_producto("Abc-1", "Cable 2", "20")
