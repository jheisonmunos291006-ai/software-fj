from abc import ABC, abstractmethod
from entidades import Entidad
from excepciones import ErrorValidacion, ServicioNoDisponibleError, ErrorCostoError
from logger import registrar_evento


class Servicio(Entidad, ABC):
    def __init__(self, identificador, nombre, tarifa, disponible=True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise ErrorValidacion("Nombre de servicio inválido.")
        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise ErrorValidacion("La tarifa debe ser un número mayor que cero.")
        self._nombre = nombre.strip()
        self._tarifa = float(tarifa)
        self._disponible = bool(disponible)

    @property
    def nombre(self): return self._nombre
    @property
    def tarifa(self): return self._tarifa
    @property
    def disponible(self): return self._disponible

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    # Variantes de cálculo: base, con descuento, con descuento e impuesto.
    def calcular_costo(self, unidades=1, descuento=0, impuesto=0):
        self.verificar_disponibilidad()
        if unidades <= 0 or descuento < 0 or descuento > 100 or impuesto < 0:
            raise ErrorCostoError("Parámetros inválidos para calcular el costo.")
        subtotal = self._tarifa * unidades
        total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)
        if total < 0:
            raise ErrorCostoError("El cálculo produjo un valor negativo.")
        return round(total, 2)

    @abstractmethod
    def validar_parametros(self, duracion): pass

    @abstractmethod
    def describir(self): pass


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad < 1:
            raise ErrorValidacion("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0 or duracion > 12:
            raise ErrorValidacion("La reserva de sala debe durar entre 0 y 12 horas.")
        return True


    def calcular_costo(self, unidades=1, descuento=0, impuesto=0):
        self.validar_parametros(unidades)
        return super().calcular_costo(unidades, descuento, impuesto)


    def describir(self):
        return f"Sala: {self.nombre} | Tarifa/hora: ${self.tarifa:,.0f} | Capacidad: {self._capacidad} personas"

class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_dia, unidades_stock, disponible=True):
        super().__init__(identificador, nombre, tarifa_dia, disponible)
        if not isinstance(unidades_stock, int) or unidades_stock < 0:
            raise ErrorValidacion("El stock debe ser un entero igual o mayor a cero.")
        self._stock = unidades_stock

    @property
    def stock(self): return self._stock


    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0 or duracion > 30:
            raise ErrorValidacion("El alquiler debe ser entre 1 y 30 días.")
        if self._stock < 1:
            raise ServicioNoDisponibleError(f"No hay unidades disponibles de {self.nombre}.")
        return True


    def descontar_stock(self, cantidad=1):
        if cantidad < 1 or cantidad > self._stock:
            raise ServicioNoDisponibleError("Cantidad solicitada no disponible.")
        self._stock -= cantidad

    def reponer_stock(self, cantidad=1):
        self._stock += cantidad

    def calcular_costo(self, unidades=1, descuento=0, impuesto=0):
        self.validar_parametros(unidades)
        return super().calcular_costo(unidades, descuento, impuesto)

    def describir(self):
        return f"Equipo: {self.nombre} | Tarifa/día: ${self.tarifa:,.0f} | Stock: {self._stock}"

class Asesoria(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ErrorValidacion("La especialidad no puede estar vacía.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0 or duracion > 8:
            raise ErrorValidacion("La asesoría debe durar entre 0 y 8 horas.")
        return True


    def calcular_costo(self, unidades=1, descuento=0, impuesto=0):
        self.validar_parametros(unidades)
        return super().calcular_costo(unidades, descuento, impuesto)

    def describir(self):
        return f"Asesoría: {self.nombre} | Especialidad: {self._especialidad} | Tarifa/hora: ${self.tarifa:,.0f}"
