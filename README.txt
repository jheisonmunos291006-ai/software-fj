SOFTWARE FJ - SISTEMA DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS

Requisitos: Python 3.9 o superior. No usa base de datos ni librerias externas.

EJECUCION:
1. Extraiga la carpeta SoftwareFJ.
2. Abra la carpeta en VS Code.
3. Abra una terminal dentro de la carpeta.
4. Ejecute: python main.py
5. En el menu, elija 8 para realizar demostracion automatizada.

ARCHIVOS:
main.py          Menu, demostracion de operaciones y flujo de ejecucion.
entidades.py     Entidad abstracta y Cliente encapsulado.
servicios.py     Servicio abstracto y tres tipos concretos.
reservas.py      Reserva, estados, confirmacion y cancelacion.
gestor.py       Listas internas y operaciones centralizadas.
excepciones.py   Excepciones personalizadas.
logger.py        Registro de eventos y errores en logs/eventos.log.
logs/           Archivo de registro creado automaticamente.

NOTA SOBRE SOBRECARGA:
Python no soporta sobrecarga tradicional por firma como Java/C++. Se demuestra una
variante flexible del metodo calcular_costo mediante parametros opcionales: unidades,
descuento e impuesto. El mismo metodo se adapta a distintas formas de calcular el costo.

NOTA SOBRE DEMOSTRACION:
La opcion 8 ejecuta escenarios exitosos e incorrectos. Incluye un error de tiempo
intencional (minutos tratados como horas) para demostrar deteccion, registro y
continuidad del programa. El error es solo de demostracion y no afecta reservas reales.
