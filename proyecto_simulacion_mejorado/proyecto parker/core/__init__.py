"""
Módulo core - Núcleo de la aplicación de simulación
Contiene la lógica principal de generación, distribuciones y análisis
"""

from .generadores import GeneradorPseudoaleatorio
from .distribuciones import DistribucionDiscreta, DistribucionContinua
from .pruebas_bondad import PruebasBondad
from .monte_carlo import MonteCarlo

__all__ = [
    'GeneradorPseudoaleatorio',
    'DistribucionDiscreta', 
    'DistribucionContinua',
    'PruebasBondad',
    'MonteCarlo'
]