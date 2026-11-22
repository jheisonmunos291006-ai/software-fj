class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""

class ErrorValidacion(SoftwareFJError):
    pass

class ClienteDuplicadoError(SoftwareFJError):
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    pass

class ReservaInvalidaError(SoftwareFJError):
    pass

class EstadoReservaError(SoftwareFJError):
    pass

class ErrorCostoError(SoftwareFJError):
    pass
