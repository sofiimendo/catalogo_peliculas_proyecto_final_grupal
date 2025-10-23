# pelicula.py
from dataclasses import dataclass

@dataclass
class Pelicula:
    # Atributo privado (requisito del enunciado)
    __nombre: str

    def __init__(self, nombre: str):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la película no puede estar vacío.")
        # normalizamos espacios internos
        self.__nombre = " ".join(nombre.split())

    # Propiedad solo-lectura para exponer el nombre de forma controlada
    @property
    def nombre(self) -> str:
        return self.__nombre

    # Representación en archivo (una película por línea)
    def to_line(self) -> str:
        return self.__nombre

    # Creador desde línea de archivo
    @staticmethod
    def from_line(line: str) -> "Pelicula":
        return Pelicula(line.strip())

    def __str__(self) -> str:
        return self.__nombre
