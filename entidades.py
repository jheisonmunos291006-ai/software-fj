from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import ErrorValidacion
from logger import registrar_evento

class Entidad(ABC):
    def __init__(self, identificador):
        if not identificador or not str(identificador).strip():
            raise ErrorValidacion("El identificador no puede estar vacío.")
        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        pass

class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.__nombre = self._validar_nombre(nombre)
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)
        self.__fecha_registro = datetime.now()
        registrar_evento(f"Cliente registrado: {self.identificador} - {self.__nombre}")

    @staticmethod
    def _validar_nombre(nombre):
        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise ErrorValidacion("El nombre debe contener al menos 2 caracteres.")
        return nombre.strip()

    @staticmethod
    def _validar_correo(correo):
        if not isinstance(correo, str) or "@" not in correo or "." not in correo.split("@")[-1]:
            raise ErrorValidacion("Correo inválido. Ejemplo válido: cliente@email.com")
        return correo.strip().lower()

    @staticmethod
    def _validar_telefono(telefono):
        digitos = "".join(c for c in str(telefono) if c.isdigit())
        if len(digitos) < 7 or len(digitos) > 15:
            raise ErrorValidacion("El teléfono debe tener entre 7 y 15 dígitos.")
        return digitos


    @property
    def nombre(self): return self.__nombre
    @property
    def correo(self): return self.__correo
    @property
    def telefono(self): return self.__telefono
    @property
    def fecha_registro(self): return self.__fecha_registro


    def describir(self):
        return f"Cliente [{self.identificador}] | {self.__nombre} | {self.__correo} | Tel: {self.__telefono}"
