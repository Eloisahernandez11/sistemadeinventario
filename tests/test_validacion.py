"""Validación de datos: se aceptan datos correctos y se rechazan los incorrectos."""

import pytest

from inventario import ExistenciaInsuficienteError, ValidacionError

pytestmark = pytest.mark.validacion


@pytest.mark.parametrize("codigo", ["", "   ", None, "A B", "COD*1", "X" * 21])
def test_cp09_rechaza_codigo_invalido(servicio, codigo):
    with pytest.raises(ValidacionError):
        servicio.registrar_producto(codigo, "Producto", "10")


@pytest.mark.parametrize("nombre", ["", "   ", None, "N" * 101])
def test_cp09_rechaza_nombre_invalido(servicio, nombre):
    with pytest.raises(ValidacionError):
        servicio.registrar_producto("P001", nombre, "10")


@pytest.mark.parametrize("precio", [-1, "-0.01", "abc", "", None, True, "nan", "inf"])
def test_cp10_rechaza_precio_invalido(servicio, precio):
    with pytest.raises(ValidacionError):
        servicio.registrar_producto("P001", "Producto", precio)


@pytest.mark.parametrize("existencia", [-1, "-5", "diez", 2.5, True, None])
def test_cp10_rechaza_existencia_inicial_invalida(servicio, existencia):
    with pytest.raises(ValidacionError):
        servicio.registrar_producto("P001", "Producto", "10", existencia)


@pytest.mark.parametrize("cantidad", [0, -3, "x", 1.5, None, True])
def test_cp11_rechaza_cantidad_invalida_en_movimientos(con_producto, cantidad):
    with pytest.raises(ValidacionError):
        con_producto.registrar_entrada("P001", cantidad)
    with pytest.raises(ValidacionError):
        con_producto.registrar_salida("P001", cantidad)
    assert con_producto.consultar_existencia("P001") == 10


def test_cp12_rechaza_salida_mayor_que_la_existencia(con_producto):
    with pytest.raises(ExistenciaInsuficienteError) as error:
        con_producto.registrar_salida("P001", 11)

    assert error.value.disponible == 10
    assert error.value.solicitada == 11
    assert con_producto.consultar_existencia("P001") == 10
    assert con_producto.historial("P001") == []


def test_modificar_rechaza_datos_invalidos_sin_alterar_el_producto(con_producto):
    with pytest.raises(ValidacionError):
        con_producto.modificar_producto("P001", precio="-5")

    assert str(con_producto.consultar_producto("P001").precio) == "100.00"


def test_acepta_precio_cero_y_redondea_a_dos_decimales(servicio):
    gratis = servicio.registrar_producto("P001", "Muestra", 0)
    redondeado = servicio.registrar_producto("P002", "Cable", "10.126")

    assert str(gratis.precio) == "0.00"
    assert str(redondeado.precio) == "10.13"
