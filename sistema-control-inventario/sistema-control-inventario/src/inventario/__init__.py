"""Sistema de Control de Inventario."""

from .errors import (
    ExistenciaInsuficienteError,
    InventarioError,
    ProductoDuplicadoError,
    ProductoNoEncontradoError,
    ValidacionError,
)
from .models import Movimiento, Producto
from .repository import RepositorioSQLite
from .reporte import Reporte
from .service import InventarioService

__all__ = [
    "ExistenciaInsuficienteError",
    "InventarioError",
    "InventarioService",
    "Movimiento",
    "Producto",
    "ProductoDuplicadoError",
    "ProductoNoEncontradoError",
    "Reporte",
    "RepositorioSQLite",
    "ValidacionError",
]
__version__ = "1.0.0"
