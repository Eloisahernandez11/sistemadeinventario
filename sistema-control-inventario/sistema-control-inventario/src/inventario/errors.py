"""Excepciones del dominio del inventario."""


class InventarioError(Exception):
    """Clase base de todos los errores controlados del sistema."""


class ValidacionError(InventarioError):
    """Un dato de entrada no cumple las reglas de validación."""


class ProductoDuplicadoError(InventarioError):
    """Ya existe un producto con el mismo código."""

    def __init__(self, codigo: str) -> None:
        super().__init__(f"Ya existe un producto con el código '{codigo}'.")
        self.codigo = codigo


class ProductoNoEncontradoError(InventarioError):
    """No existe un producto con el código indicado."""

    def __init__(self, codigo: str) -> None:
        super().__init__(f"Producto no encontrado: '{codigo}'.")
        self.codigo = codigo


class ExistenciaInsuficienteError(InventarioError):
    """La salida solicitada es mayor que la existencia disponible."""

    def __init__(self, codigo: str, disponible: int, solicitada: int) -> None:
        super().__init__(
            f"Existencia insuficiente para '{codigo}': "
            f"disponible {disponible}, solicitada {solicitada}."
        )
        self.codigo = codigo
        self.disponible = disponible
        self.solicitada = solicitada
