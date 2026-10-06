import pytest

from inventario import InventarioService, RepositorioSQLite


@pytest.fixture
def repo():
    repositorio = RepositorioSQLite(":memory:")
    yield repositorio
    repositorio.cerrar()


@pytest.fixture
def servicio(repo):
    return InventarioService(repo)


@pytest.fixture
def con_producto(servicio):
    """Servicio con un producto P001 (precio 100.00, existencia 10)."""
    servicio.registrar_producto("P001", "Teclado USB", "100.00", 10, "Teclado español")
    return servicio
