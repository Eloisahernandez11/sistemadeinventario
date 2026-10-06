"""Reglas de validación de los datos de entrada."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

from .errors import ValidacionError

_PATRON_CODIGO = re.compile(r"^[A-Z0-9_-]{1,20}$")
_MAX_NOMBRE = 100
_MAX_DESCRIPCION = 255
_CENTAVOS = Decimal("0.01")


def validar_codigo(valor: object) -> str:
    """El código se normaliza a mayúsculas: 1-20 letras, números, '-' o '_'."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValidacionError("El código es obligatorio.")
    codigo = valor.strip().upper()
    if not _PATRON_CODIGO.match(codigo):
        raise ValidacionError(
            "El código solo admite letras, números, '-' y '_' (máximo 20 caracteres)."
        )
    return codigo


def validar_nombre(valor: object) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ValidacionError("El nombre es obligatorio.")
    nombre = valor.strip()
    if len(nombre) > _MAX_NOMBRE:
        raise ValidacionError(f"El nombre no puede exceder {_MAX_NOMBRE} caracteres.")
    return nombre


def validar_descripcion(valor: object) -> str:
    if valor is None:
        return ""
    if not isinstance(valor, str):
        raise ValidacionError("La descripción debe ser texto.")
    descripcion = valor.strip()
    if len(descripcion) > _MAX_DESCRIPCION:
        raise ValidacionError(
            f"La descripción no puede exceder {_MAX_DESCRIPCION} caracteres."
        )
    return descripcion


def validar_precio(valor: object) -> Decimal:
    """El precio debe ser un número >= 0; se redondea a 2 decimales."""
    if isinstance(valor, bool) or valor is None:
        raise ValidacionError("El precio debe ser un número.")
    try:
        precio = Decimal(str(valor).strip())
    except (InvalidOperation, ValueError):
        raise ValidacionError("El precio debe ser un número.") from None
    if not precio.is_finite():
        raise ValidacionError("El precio debe ser un número.")
    if precio < 0:
        raise ValidacionError("El precio no puede ser negativo.")
    return precio.quantize(_CENTAVOS)


def _entero(valor: object, campo: str) -> int:
    if isinstance(valor, bool):
        raise ValidacionError(f"{campo} debe ser un número entero.")
    if isinstance(valor, int):
        return valor
    if isinstance(valor, str):
        try:
            return int(valor.strip())
        except ValueError:
            pass
    raise ValidacionError(f"{campo} debe ser un número entero.")


def validar_existencia(valor: object) -> int:
    """Existencia inicial: entero >= 0."""
    existencia = _entero(valor, "La existencia")
    if existencia < 0:
        raise ValidacionError("La existencia no puede ser negativa.")
    return existencia


def validar_cantidad(valor: object) -> int:
    """Cantidad de un movimiento: entero > 0."""
    cantidad = _entero(valor, "La cantidad")
    if cantidad <= 0:
        raise ValidacionError("La cantidad debe ser mayor que cero.")
    return cantidad
