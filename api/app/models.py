"""Model prediction request and response classes"""
from pydantic import BaseModel


class IncomeRequest(BaseModel):
    """Prediction request class that contains the relevant features.

    Args:
        BaseModel (BaseModel): JSON element request.
    """
    ingreso: float
    antiguedad_laboral_meses: int
    tiempo_desempleado: int
    trabajos_ultimos_5: int
    semanasCotizadas: int
    edad: int
    crecimiento_ingreso: float
    lugar_actual: int


    def values_checker(self):
        """Check input parameters.

        Returns:
            bool: True if request has correct params.
        """
        if self.ingreso < 0 or self.antiguedad_laboral_meses < 0 or self.tiempo_desempleado < 0 or \
           self.trabajos_ultimos_5 < 0 or self.semanasCotizadas < 0 or self.edad < 18 or \
           self.edad > 80 or self.lugar_actual > 31 or \
           (self.ingreso == 0 and self.crecimiento_ingreso != 0) or \
           (self.antiguedad_laboral_meses > 0 and self.tiempo_desempleado > 0):
            return False
        return True


class PredictionRequest(BaseModel):
    """Prediction request class that contains the relevant features.

    Args:
        BaseModel (BaseModel): JSON element request.
    """
    ingreso: float
    antiguedad_laboral_meses: int
    tiempo_desempleado: int
    trabajos_ultimos_5: int
    semanasCotizadas: int
    edad: int
    crecimiento_ingreso: float
    crecimiento_gral: float
    ENIGH: float


class PredictionResponse(BaseModel):
    """Prediction response class that contains the target features.

    Args:
        BaseModel (BaseModel): JSON element response.
    """
    scoring: float
    cluster: str
