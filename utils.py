# utils.py
import os
import time
from functools import wraps
from typing import Callable

# Carpeta base donde se guardan catálogos y logs
BASE_DIR_CATALOGOS = "catalogos"
os.makedirs(BASE_DIR_CATALOGOS, exist_ok=True)

# ===== Lambdas útiles =====
normalizar_espacios: Callable[[str], str] = lambda s: " ".join(s.split())
a_minusculas: Callable[[str], str] = lambda s: s.lower()

# ===== Decoradores =====
def log_accion(nombre_archivo_log: str = "acciones.log"):
    """
    Decorador que registra en catalogos/<archivo_log>:
    - nombre de la función
    - args/kwargs simples
    - timestamp
    """
    ruta_log = os.path.join(BASE_DIR_CATALOGOS, nombre_archivo_log)

    def _decorador(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                resultado = func(*args, **kwargs)
                estado = "OK"
                return resultado
            except Exception as e:
                estado = f"ERROR: {e}"
                raise
            finally:
                with open(ruta_log, "a", encoding="utf-8") as f:
                    f.write(f"[{ts}] {func.__name__} args={repr(args)} kwargs={repr(kwargs)} -> {estado}\n")
        return _wrapper
    return _decorador

def medir_tiempo(func):
    """
    Decorador simple para medir el tiempo de ejecución de una función.
    Loggea en catalogos/tiempos.log
    """
    ruta_log = os.path.join(BASE_DIR_CATALOGOS, "tiempos.log")

    @wraps(func)
    def _wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        dur = (time.perf_counter() - inicio) * 1000  # ms
        with open(ruta_log, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {func.__name__}: {dur:.2f} ms\n")
        return resultado
    return _wrapper
