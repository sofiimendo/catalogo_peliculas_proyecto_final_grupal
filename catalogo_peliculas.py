# catalogo_peliculas.py
import os
from typing import List
from pelicula import Pelicula
from utils import BASE_DIR_CATALOGOS, a_minusculas, log_accion, medir_tiempo

class CatalogoPeliculas:
    """
    - nombre: nombre lógico del catálogo
    - ruta_archivo: ruta al .txt
    Métodos:
      - agregar(Pelicula) -> bool   (usa set con lambda para evitar duplicados)
      - listar() -> List[Pelicula]  (ordenado A→Z con lambda)
      - eliminar_catalogo() -> bool
    """

    def __init__(self, nombre: str, base_dir: str = BASE_DIR_CATALOGOS):
        self.nombre = (nombre or "catalogo").strip()
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.ruta_archivo = os.path.join(self.base_dir, f"{self.nombre}.txt")

    @log_accion("acciones.log")
    @medir_tiempo
    def agregar(self, pelicula: Pelicula) -> bool:
        """
        Agrega la película si NO existe ya (case-insensitive).
        Retorna True si la agregó, False si era duplicada.
        """
        existentes = {a_minusculas(p.nombre) for p in self.listar()}
        if a_minusculas(pelicula.nombre) in existentes:
            return False
        with open(self.ruta_archivo, "a", encoding="utf-8") as f:
            f.write(pelicula.to_line() + "\n")
        return True

    @log_accion("acciones.log")
    @medir_tiempo
    def listar(self) -> List[Pelicula]:
        if not os.path.exists(self.ruta_archivo):
            return []
        # map + lambda -> Pelicula.from_line
        with open(self.ruta_archivo, "r", encoding="utf-8") as f:
            peliculas = list(map(lambda ln: Pelicula.from_line(ln.strip()), f if f else []))
        # sort con clave lambda (case-insensitive)
        peliculas.sort(key=lambda p: p.nombre.lower())
        return peliculas

    @log_accion("acciones.log")
    @medir_tiempo
    def eliminar_catalogo(self) -> bool:
        if os.path.exists(self.ruta_archivo):
            os.remove(self.ruta_archivo)
            return True
        return False
