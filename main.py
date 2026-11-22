from datetime import datetime, timedelta
from gestor import GestorSistema
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from excepciones import SoftwareFJError, ErrorValidacion, ReservaInvalidaError, ErrorCostoError
from logger import registrar_evento, registrar_error

sistema = GestorSistema()

def ejecutar_operacion(titulo, accion):
    print(f"\n--- {titulo} ---")
    try:
        resultado = accion()
    except SoftwareFJError as e:
        print(f"[ERROR CONTROLADO] {e}")
        registrar_error(f"Operación fallida: {titulo} | {e}")
    except (ValueError, TypeError, AttributeError) as e:
        print(f"[ERROR DE DATOS] {e}")
        registrar_error(f"Error de datos en: {titulo} | {e}")
    else:
        print("[OK] Operación realizada.")
        if resultado is not None:
            print(resultado)
    finally:
        print("Operación finalizada; el sistema continúa activo.")


def cargar_datos_demo():
    # TRY/EXCEPT/ELSE: registro de clientes de prueba.
    try:
        sistema.registrar_cliente(Cliente("C001", "Laura Méndez", "laura@email.com", "3001234567"))
        sistema.registrar_cliente(Cliente("C002", "Carlos Rojas", "carlos@email.com", "3101234567"))
    except Exception as e:
        registrar_error("Fallo al cargar clientes iniciales", e)
    else:
        registrar_evento("Datos iniciales cargados correctamente")

    ejecutar_operacion("Cliente inválido (correo incorrecto)", lambda: Cliente("C003", "Ana", "correo-sin-formato", "3011234567"))
    ejecutar_operacion("Cliente duplicado", lambda: sistema.registrar_cliente(Cliente("C001", "Laura Méndez", "laura@email.com", "3001234567")))
    ejecutar_operacion("Crear sala", lambda: sistema.agregar_servicio(ReservaSala("S001", "Sala de reuniones", 45000, 12)))
    ejecutar_operacion("Crear equipo", lambda: sistema.agregar_servicio(AlquilerEquipo("S002", "Proyector HD", 30000, 3)))
    ejecutar_operacion("Crear asesoría", lambda: sistema.agregar_servicio(Asesoria("S003", "Consultoría Python", 65000, "Desarrollo de software")))
    ejecutar_operacion("Servicio con tarifa inválida", lambda: ReservaSala("S004", "Sala defectuosa", -500, 10))
    ejecutar_operacion("Reserva válida", lambda: sistema.crear_reserva("R001", "C001", "S001", 2, descuento=10, impuesto=19))
    ejecutar_operacion("Reserva con cliente inexistente", lambda: sistema.crear_reserva("R002", "C999", "S001", 1))
    ejecutar_operacion("Confirmar reserva R001", lambda: sistema.buscar_reserva("R001").confirmar())
    ejecutar_operacion("Cancelar reserva R001", lambda: sistema.buscar_reserva("R001").cancelar())
    ejecutar_operacion("Cancelar reserva dos veces", lambda: sistema.buscar_reserva("R001").cancelar())
    ejecutar_operacion("Reserva de equipo", lambda: sistema.crear_reserva("R003", "C002", "S002", 2))

    # Error intencional: cálculo de duración con fórmula defectuosa.
    ejecutar_operacion("DEMO: detección de duración calculada incorrectamente", demo_error_tiempo)

    print("\n=== RESUMEN FINAL ===")
    print(f"Clientes registrados: {len(sistema.clientes)}")
    print(f"Servicios registrados: {len(sistema.servicios)}")
    print(f"Reservas creadas: {len(sistema.reservas)}")
    print("Clientes:")
    for linea in sistema.mostrar_clientes(): print("  ", linea)
    print("Servicios:")
    for linea in sistema.mostrar_servicios(): print("  ", linea)
    print("Reservas:")
    for linea in sistema.mostrar_reservas(): print("  ", linea)
    print("\nLas operaciones fallidas fueron capturadas. Consulte logs/eventos.log")


def demo_error_tiempo():
    """Demuestra un error de tiempo intencional y lo detecta con validación."""
    inicio = datetime(2026, 11, 22, 10, 0)
    fin = datetime(2026, 11, 22, 12, 30)
    duracion_correcta = (fin - inicio).total_seconds() / 3600
    # BUG intencional: se utiliza el componente de minutos como si fueran horas.
    duracion_defectuosa = (fin.hour - inicio.hour) + (fin.minute - inicio.minute)
    print(f"Duración real: {duracion_correcta:.2f} horas")
    print(f"Duración con fórmula defectuosa: {duracion_defectuosa:.2f} horas")
    if abs(duracion_defectuosa - duracion_correcta) > 0.01:
        try:
            raise ValueError("Los minutos se sumaron como horas en la fórmula de duración.")
        except ValueError as causa:
            # Encadenamiento: el error de dominio conserva su causa técnica original.
            raise ErrorCostoError("Detectado cálculo incorrecto del tiempo: la diferencia de minutos fue tratada como horas.") from causa
    return "La duración pasó la validación."


def menu():
    while True:
        print("\n" + "=" * 42)
        print("       SOFTWARE FJ - GESTIÓN DE SERVICIOS")
        print("=" * 42)
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Listar servicios")
        print("4. Crear reserva")
        print("5. Confirmar reserva")
        print("6. Cancelar reserva")
        print("7. Listar reservas")
        print("8. Ejecutar demostración de pruebas")
        print("0. Salir")
        try:
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                registrar_evento("Usuario cerró el sistema")
                print("Programa finalizado.")
                break
            elif opcion == "1":
                ejecutar_operacion("Registro de cliente", lambda: sistema.registrar_cliente(Cliente(input("ID: "), input("Nombre: "), input("Correo: "), input("Teléfono: "))))
            elif opcion == "2":
                print("\n".join(sistema.mostrar_clientes()) or "No hay clientes registrados.")
            elif opcion == "3":
                print("\n".join(sistema.mostrar_servicios()) or "No hay servicios registrados.")
            elif opcion == "4":
                ejecutar_operacion("Crear reserva", lambda: sistema.crear_reserva(input("ID reserva: "), input("ID cliente: "), input("ID servicio: "), float(input("Duración (horas/días según servicio): "))))
            elif opcion == "5":
                ejecutar_operacion("Confirmar reserva", lambda: sistema.buscar_reserva(input("ID reserva: ")).confirmar())
            elif opcion == "6":
                ejecutar_operacion("Cancelar reserva", lambda: sistema.buscar_reserva(input("ID reserva: ")).cancelar())
            elif opcion == "7":
                print("\n".join(sistema.mostrar_reservas()) or "No hay reservas registradas.")
            elif opcion == "8":
                cargar_datos_demo()
            else:
                print("Opción no válida. Intente nuevamente.")
        except Exception as e:
            print(f"No se pudo completar la entrada: {e}")
            registrar_error("Error no previsto en el menú", e)
            print("El sistema continúa ejecutándose.")

if __name__ == "__main__":
    registrar_evento("Inicio de Software FJ")
    menu()
