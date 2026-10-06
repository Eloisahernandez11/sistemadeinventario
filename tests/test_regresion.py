"""Pruebas de regresión: protegen comportamientos que ya funcionan."""

from decimal import Decimal

import pytest

from inventario import ExistenciaInsuficienteError

pytestmark = pytest.mark.regresion


def test_vaciar_el_inventario_deja_existencia_cero_y_no_negativa(con_producto):
    con_producto.registrar_salida("P001", 10)

    assert con_producto.consultar_existencia("P001") == 0
    with pytest.raises(ExistenciaInsuficienteError):
        con_producto.registrar_salida("P001", 1)
    assert con_producto.consultar_existencia("P001") == 0


def test_modificar_producto_no_altera_su_existencia(con_producto):
    con_producto.registrar_entrada("P001", 5)

    con_producto.modificar_producto("P001", nombre="Nuevo nombre", precio="1")

    assert con_producto.consultar_existencia("P001") == 15


def test_se_puede_registrar_de_nuevo_un_codigo_eliminado(con_producto):
    con_producto.eliminar_producto("P001")

    nuevo = con_producto.registrar_producto("P001", "Teclado nuevo", "80", 2)

    assert nuevo.existencia == 2
    assert con_producto.consultar_producto("P001").precio == Decimal("80.00")


def test_entradas_y_salidas_alternadas_mantienen_la_suma_correcta(con_producto):
    for cantidad in (3, 7, 1):
        con_producto.registrar_entrada("P001", cantidad)
        con_producto.registrar_salida("P001", cantidad - 1 if cantidad > 1 else 1)

    # 10 + (3-2) + (7-6) + (1-1) = 12
    assert con_producto.consultar_existencia("P001") == 12
