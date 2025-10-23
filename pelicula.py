# pelicula.py
from dataclasses import dataclass
from utils import normalizar_espacios

@dataclass
class Obra:
    # Atributo privado exigido por el enunciado
    __nombre: str

    def __init__(self, nombre: str):
        nombre = (nombre or "").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = normalizar_espacios(nombre)

    @property
    def nombre(self) -> str:
        return self.__nombre

    def to_line(self) -> str:
        return self.__nombre

    @staticmethod
    def from_line(linea: str) -> "Obra":
        return Obra(linea.strip())

    def __str__(self) -> str:
        return self.__nombre

@dataclass
class Pelicula(Obra):
    """
    Subclase concreta. En el futuro podrían agregar campos como 'género' o 'año'.
    Por ahora hereda toda la lógica de Obra.
    """
    pass
