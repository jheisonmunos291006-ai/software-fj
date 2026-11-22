from datetime import datetime
from excepciones import ReservaInvalidaError, EstadoReservaError, ErrorValidacion
from logger import registrar_evento

class Reserva:
    ESTADOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA")
    def __init__(self, identificador, cliente, servicio, duracion, descuento=0, impuesto=0):
        if not identificador:
            raise ReservaInvalidaError("La reserva requiere identificador.")
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("Debe asignar cliente y servicio a la reserva.")
        servicio.verificar_disponibilidad()
        servicio.validar_parametros(duracion)
        self._id = str(identificador)
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._descuento = descuento
        self._impuesto = impuesto
        self._estado = "PENDIENTE"
        self._creada = datetime.now()
        self._total = servicio.calcular_costo(duracion, descuento, impuesto)
        registrar_evento(f"Reserva creada {self._id}, estado PENDIENTE, total ${self._total:.2f}")

    @property
    def id(self): return self._id
    @property
    def cliente(self): return self._cliente
    @property
    def servicio(self): return self._servicio
    @property
    def duracion(self): return self._duracion
    @property
    def estado(self): return self._estado
    @property
    def total(self): return self._total

    def confirmar(self):
        if self._estado != "PENDIENTE":
            raise EstadoReservaError(f"No se puede confirmar una reserva en estado {self._estado}.")
        self._servicio.verificar_disponibilidad()
        if self._servicio.__class__.__name__ == "AlquilerEquipo":
            self._servicio.descontar_stock(1)
        self._estado = "CONFIRMADA"
        registrar_evento(f"Reserva {self._id} confirmada")
        return True


    def cancelar(self):
        if self._estado == "CANCELADA":
            raise EstadoReservaError(f"La reserva {self._id} ya está cancelada.")
        if self._estado == "CONFIRMADA" and self._servicio.__class__.__name__ == "AlquilerEquipo":
            self._servicio.reponer_stock(1)
        self._estado = "CANCELADA"
        registrar_evento(f"Reserva {self._id} cancelada")
        return True


    def describir(self):
        return f"Reserva {self._id} | Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | Duración: {self._duracion} | Estado: {self._estado} | Total: ${self._total:,.2f}"
