from entidades import Cliente
from servicios import Servicio
from reservas import Reserva
from excepciones import ClienteDuplicadoError, ErrorValidacion, ReservaInvalidaError
from logger import registrar_evento, registrar_error

class GestorSistema:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    @property
    def clientes(self): return tuple(self._clientes)
    @property
    def servicios(self): return tuple(self._servicios)
    @property
    def reservas(self): return tuple(self._reservas)

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ErrorValidacion("El objeto recibido no es un Cliente válido.")
        if any(c.identificador == cliente.identificador or c.correo == cliente.correo for c in self._clientes):
            raise ClienteDuplicadoError("Ya existe un cliente con ese ID o correo.")
        self._clientes.append(cliente)
        registrar_evento(f"Cliente agregado a lista del gestor: {cliente.identificador}")
        return cliente


    def agregar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ErrorValidacion("El objeto recibido no corresponde a un Servicio.")
        if any(s.identificador == servicio.identificador for s in self._servicios):
            raise ErrorValidacion("Ya existe un servicio con ese identificador.")
        self._servicios.append(servicio)
        registrar_evento(f"Servicio agregado: {servicio.identificador}")
        return servicio


    def crear_reserva(self, id_reserva, id_cliente, id_servicio, duracion, descuento=0, impuesto=0):
        cliente = next((c for c in self._clientes if c.identificador == str(id_cliente)), None)
        servicio = next((s for s in self._servicios if s.identificador == str(id_servicio)), None)
        if cliente is None:
            raise ReservaInvalidaError(f"Cliente '{id_cliente}' no encontrado.")
        if servicio is None:
            raise ReservaInvalidaError(f"Servicio '{id_servicio}' no encontrado.")
        reserva = Reserva(id_reserva, cliente, servicio, duracion, descuento, impuesto)
        if any(r.id == reserva.id for r in self._reservas):
            raise ReservaInvalidaError(f"La reserva '{reserva.id}' ya existe.")
        self._reservas.append(reserva)
        return reserva

    def buscar_reserva(self, id_reserva):
        reserva = next((r for r in self._reservas if r.id == str(id_reserva)), None)
        if reserva is None:
            raise ReservaInvalidaError(f"Reserva '{id_reserva}' no encontrada.")
        return reserva


    def mostrar_clientes(self): return [c.describir() for c in self._clientes]
    def mostrar_servicios(self): return [s.describir() for s in self._servicios]
    def mostrar_reservas(self): return [r.describir() for r in self._reservas]
