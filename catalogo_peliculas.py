# catalogo_peliculas.py
import os
from typing import List
from pelicula import Pelicula

class CatalogoPeliculas:
    """
    Implementa la lógica de manejo de catálogos:
    - atributo nombre (nombre lógico del catálogo)
    - atributo ruta_archivo (ruta al .txt donde se guardan las películas)
    - métodos: agregar, listar, eliminar
    """
    def __init__(self, nombre: str, base_dir: str = "catalogos"):
        self.nombre = nombre.strip() or "catalogo"
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.ruta_archivo = os.path.join(self.base_dir, f"{self.nombre}.txt")

    def agregar(self, pelicula: Pelicula) -> None:
        with open(self.ruta_archivo, "a", encoding="utf-8") as f:
            f.write(pelicula.to_line() + "\n")

    def listar(self) -> List[Pelicula]:
        if not os.path.exists(self.ruta_archivo):
            return []
        peliculas: List[Pelicula] = []
        with open(self.ruta_archivo, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    peliculas.append(Pelicula.from_line(line))
        return peliculas

    def eliminar_catalogo(self) -> bool:
        """
        Elimina el archivo .txt asociado al catálogo.
        Retorna True si lo eliminó; False si no existía.
        """
        if os.path.exists(self.ruta_archivo):
            os.remove(self.ruta_archivo)
            return True
        return False
