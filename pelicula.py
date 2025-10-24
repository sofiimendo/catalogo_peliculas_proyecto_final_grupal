# pelicula.py
from dataclasses import dataclass
from utils import normalizar_espacios

# ======== CLASE BASE ========

@dataclass
class Film:
    """
    Clase base para representar una filmación o película genérica.
    Atributo privado: __nombre
    """

    __nombre: str  # atributo privado

    def __init__(self, nombre: str):
        nombre = (nombre or "").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = normalizar_espacios(nombre)

    # ---- Propiedad de solo lectura ----
    @property
    def nombre(self) -> str:
        """Propiedad solo lectura para acceder al nombre."""
        return self.__nombre

    # ---- Conversión para guardar / leer ----
    def to_line(self) -> str:
        """Convierte la filmación en una línea de texto para guardar en archivo."""
        return self.__nombre

    @staticmethod
    def from_line(linea: str) -> "Film":
        """Crea un Film a partir de una línea del archivo."""
        return Film(linea.strip())

    def __str__(self) -> str:
        """Cómo se muestra el objeto al imprimirlo."""
        return self.__nombre


# ======== SUBCLASE PELICULA ========

@dataclass
class Pelicula(Film):
    """
    Subclase concreta de Film que representa una Película.
    Hereda el atributo privado __nombre y agrega:
    - género
    - año de estreno
    """

    genero: str = "Desconocido"
    anio: int = 0

    def __init__(self, nombre: str, genero: str = "Desconocido", anio: int = 0):
        super().__init__(nombre)
        self.genero = normalizar_espacios(genero or "Desconocido").capitalize()
        try:
            self.anio = int(anio)
        except ValueError:
            self.anio = 0

    # ---- Sobrescribimos to_line() para guardar más info ----
    def to_line(self) -> str:
        """
        Guarda en formato: nombre | genero | año
        """
        return f"{self.nombre} | {self.genero} | {self.anio}"

    @staticmethod
    def from_line(linea: str) -> "Pelicula":
        """
        Crea una Pelicula desde una línea guardada.
        Permite compatibilidad con catálogos viejos (solo nombre).
        """
        partes = [p.strip() for p in linea.split("|")]
        if len(partes) == 1:
            # versión vieja (solo nombre)
            return Pelicula(partes[0])
        elif len(partes) >= 3:
            nombre, genero, anio = partes[:3]
            return Pelicula(nombre, genero, anio)
        else:
            return Pelicula(partes[0])

    def __str__(self) -> str:
        """Muestra nombre, género y año al listar."""
        if self.anio > 0:
            return f"{self.nombre} ({self.genero}, {self.anio})"
        return f"{self.nombre} ({self.genero})"
