# catalogo_peliculas.py
import os
from typing import List
from pelicula import Pelicula
from utils import BASE_DIR_CATALOGOS, a_minusculas, log_accion, medir_tiempo

class CatalogoPeliculas:
    """
    Administra un catálogo de películas con persistencia en archivo .txt.

    Características clave:
    - Generadores:
        * _iter_lineas(): recorre el archivo línea a línea (lazy)
        * iter_peliculas(): genera objetos Pelicula en streaming
    - Decoradores:
        * @log_accion y @medir_tiempo para logging y performance
    - Lambdas:
        * a_minusculas() para comparaciones case-insensitive
        * sort(key=lambda ...) para ordenar A→Z
    """

    def __init__(self, nombre: str, base_dir: str = BASE_DIR_CATALOGOS):
        self.nombre = (nombre or "catalogo").strip()
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.ruta_archivo = os.path.join(self.base_dir, f"{self.nombre}.txt")

    # --- GENERADORES ---

    def _iter_lineas(self):
        """
        Generador que devuelve una línea 'limpia' por vez del archivo del catálogo.
        Ventaja: lectura perezosa (no carga todo en memoria).
        """
        if not os.path.exists(self.ruta_archivo):
            return
        with open(self.ruta_archivo, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield line  # genera una línea válida por vez

    def iter_peliculas(self):
        """
        Generador de objetos Pelicula, a partir de _iter_lineas().
        """
        for linea in self._iter_lineas():
            yield Pelicula.from_line(linea)  # genera Pelicula en streaming

    # --- OPERACIONES PRINCIPALES ---

    @log_accion("acciones.log")
    @medir_tiempo
    def agregar(self, pelicula: Pelicula) -> bool:
        """
        Agrega la película si NO existe ya (case-insensitive).
        Usa una generator expression para chequear duplicados en streaming.
        Retorna True si la agregó, False si era duplicada.
        """
        existentes = (a_minusculas(p.nombre) for p in self.iter_peliculas())
        if a_minusculas(pelicula.nombre) in existentes:  # 'in' consume el generador hasta encontrar o agotar
            return False

        with open(self.ruta_archivo, "a", encoding="utf-8") as f:
            f.write(pelicula.to_line() + "\n")
        return True

    @log_accion("acciones.log")
    @medir_tiempo
    def listar(self) -> List[Pelicula]:
        """
        Devuelve una lista materializada, pero la lectura del archivo
        se hace con generadores (lazy). Luego ordena A→Z.
        """
        peliculas = list(self.iter_peliculas())  # consume el generador
        peliculas.sort(key=lambda p: p.nombre.lower())
        return peliculas

    @log_accion("acciones.log")
    @medir_tiempo
    def eliminar_catalogo(self) -> bool:
        """
        Elimina el archivo .txt asociado al catálogo.
        Retorna True si lo eliminó; False si no existía.
        """
        if os.path.exists(self.ruta_archivo):
            os.remove(self.ruta_archivo)
            return True
        return False
