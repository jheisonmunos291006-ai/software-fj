class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""

class ErrorValidacion(SoftwareFJError):
    pass
    #DATOS QUE NO CUMPLEN LAS REGLAS#
class ClienteDuplicadoError(SoftwareFJError):
    pass
    #CUANDO SE INTENTA REGISTRAR UN CLIENTE QUE YA EXISTE#
class ServicioNoDisponibleError(SoftwareFJError):
    pass
    #CUANDO SE INTENTA SOLICITAR UN SERVICIO NO DISPONIBLE#
class ReservaInvalidaError(SoftwareFJError):
    pass
    #CREAR UNA RESERVA CON DATOS INCORRECTOS#
class EstadoReservaError(SoftwareFJError):
    pass
    #OPERAR UNA RESERVA EN UN ESTADO NO PERMITIDO#
class ErrorCostoError(SoftwareFJError):
    pass
    #PROBLEMAS AL CALCULAR EL COSTO#
