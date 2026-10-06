# Casos de prueba

Cada caso está automatizado con pytest; el nombre de la prueba empieza con el ID del caso
(por ejemplo `test_cp01_...`). Para ver todos: `pytest -v`.

Los resultados de la tabla se obtuvieron con `pytest` en Python 3.13 el 6 de octubre de 2026
(57 pruebas, todas aprobadas). **Vuelvan a ejecutar `pytest -v` en su equipo y adjunten su propia captura.**

## Casos requeridos

| ID | Funcionalidad | Entrada | Resultado esperado | Resultado obtenido | Estado | Prueba automatizada |
|---|---|---|---|---|---|---|
| CP-01 | Registrar producto | Datos válidos: código `P001`, nombre, precio `150.50`, existencia 5 | Producto registrado | Producto registrado con precio 150.50 y existencia 5 | Aprobada | `test_cp01_registrar_producto_con_datos_validos` |
| CP-02 | Registrar producto | Código duplicado `P001` | Mostrar error | `ProductoDuplicadoError`: "Ya existe un producto con el código 'P001'"; el producto original no cambió | Aprobada | `test_cp02_registrar_producto_con_codigo_duplicado` |
| CP-03 | Consultar producto | Código existente `P001` | Mostrar producto | Devuelve nombre "Teclado USB" y existencia 10 | Aprobada | `test_cp03_consultar_producto_con_codigo_existente` |
| CP-04 | Consultar producto | Código inexistente | Mostrar mensaje | `ProductoNoEncontradoError`: "Producto no encontrado" | Aprobada | `test_cp04_consultar_producto_con_codigo_inexistente` |
| CP-05 | Modificar producto | `P001` con nombre y precio nuevos válidos | Información actualizada | Nombre y precio actualizados; descripción y existencia intactas | Aprobada | `test_cp05_modificar_producto_con_datos_validos` |
| CP-06 | Eliminar producto | `P001` existente | Producto eliminado | El producto ya no aparece en consultas ni en el listado | Aprobada | `test_cp06_eliminar_producto_existente` |
| CP-07 | Entrada de producto | `P001`, cantidad 5 | Incrementar existencia | Existencia 10 → 15 | Aprobada | `test_cp07_entrada_con_cantidad_valida_incrementa_existencia` |
| CP-08 | Salida de producto | `P001`, cantidad 4 (disponible 10) | Reducir existencia | Existencia 10 → 6 | Aprobada | `test_cp08_salida_con_cantidad_disponible_reduce_existencia` |

## Casos adicionales

| ID | Funcionalidad | Entrada | Resultado esperado | Resultado obtenido | Estado | Prueba automatizada |
|---|---|---|---|---|---|---|
| CP-09 | Validar código y nombre | Vacío, solo espacios, nulo, caracteres no permitidos o demasiado largo | Rechazar con error de validación | `ValidacionError` en todos los casos; no se registra nada | Aprobada | `test_cp09_*` |
| CP-10 | Validar precio y existencia inicial | Precio negativo, texto, `nan`, `inf`; existencia negativa, decimal o texto | Rechazar con error de validación | `ValidacionError` en todos los casos | Aprobada | `test_cp10_*` |
| CP-11 | Validar cantidad de movimiento | 0, negativa, texto, decimal o nula | Rechazar sin cambiar la existencia | `ValidacionError`; existencia sigue en 10 | Aprobada | `test_cp11_*` |
| CP-12 | Salida mayor a la existencia | `P001`, cantidad 11 (disponible 10) | Rechazar y no cambiar la existencia | `ExistenciaInsuficienteError` (disponible 10, solicitada 11); sin movimiento en el historial | Aprobada | `test_cp12_rechaza_salida_mayor_que_la_existencia` |
| CP-13 | Reporte de inventario | 3 productos con entradas y salidas | Totales correctos | 3 productos, 15 unidades, valor total 1500.00, 2 sin existencia | Aprobada | `test_cp13_reporte_despues_de_registrar_movimientos` |

## Pruebas de integración y regresión

| Archivo | Qué comprueba |
|---|---|
| `tests/test_integracion.py` | Los datos persisten entre sesiones; flujo completo por CLI; errores controlados con código de salida 1 |
| `tests/test_regresion.py` | La existencia nunca queda negativa; modificar no altera existencias; se puede reutilizar un código eliminado; entradas y salidas alternadas suman bien |

## Cómo registrar una incidencia

Si una prueba falla, crear una tarjeta en Trello (columna *Pendiente*) con: ID del caso, entrada usada,
resultado esperado, resultado obtenido y captura. Marcar el caso como **No aprobada** hasta verificar la corrección.
