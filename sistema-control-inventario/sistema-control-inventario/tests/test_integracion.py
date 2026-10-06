"""Pruebas de integración: servicio + repositorio SQLite en disco + CLI."""

import pytest

from inventario import InventarioService, RepositorioSQLite
from inventario.cli import main

pytestmark = pytest.mark.integracion


def test_los_datos_persisten_entre_sesiones(tmp_path):
    ruta = str(tmp_path / "inv.db")

    primera = RepositorioSQLite(ruta)
    InventarioService(primera).registrar_producto("P001", "Mouse", "99.90", 3)
    InventarioService(primera).registrar_entrada("P001", 2)
    primera.cerrar()

    segunda = RepositorioSQLite(ruta)
    servicio = InventarioService(segunda)
    assert servicio.consultar_existencia("P001") == 5
    assert len(servicio.historial()) == 1
    segunda.cerrar()


def test_flujo_completo_por_cli(tmp_path, capsys):
    db = str(tmp_path / "cli.db")

    def ejecutar(*argumentos):
        codigo = main(["--db", db, *argumentos])
        captura = capsys.readouterr()
        return codigo, captura.out, captura.err

    assert ejecutar("registrar", "P001", "Mouse USB", "150.50", "--existencia", "10")[0] == 0
    assert ejecutar("entrada", "P001", "5", "--motivo", "Compra")[0] == 0
    assert ejecutar("salida", "P001", "3")[0] == 0

    codigo, salida, _ = ejecutar("existencia", "P001")
    assert codigo == 0 and "12" in salida

    codigo, salida, _ = ejecutar("modificar", "P001", "--precio", "200")
    assert codigo == 0 and "200.00" in salida

    codigo, salida, _ = ejecutar("reporte")
    assert codigo == 0
    assert "Valor total           : 2400.00" in salida  # 12 x 200

    assert ejecutar("eliminar", "P001")[0] == 0
    assert ejecutar("consultar", "P001")[0] == 1


def test_cli_muestra_errores_controlados_y_devuelve_1(tmp_path, capsys):
    db = str(tmp_path / "cli.db")
    main(["--db", db, "registrar", "P001", "Mouse", "10", "--existencia", "1"])
    capsys.readouterr()

    assert main(["--db", db, "registrar", "P001", "Otro", "5"]) == 1
    assert "Ya existe un producto" in capsys.readouterr().err

    assert main(["--db", db, "salida", "P001", "9"]) == 1
    assert "Existencia insuficiente" in capsys.readouterr().err

    assert main(["--db", db, "entrada", "P001", "-2"]) == 1
    assert "mayor que cero" in capsys.readouterr().err
