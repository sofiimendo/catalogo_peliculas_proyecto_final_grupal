# app.py
import os
from pelicula import Pelicula
from catalogo_peliculas import CatalogoPeliculas
from utils import normalizar_espacios, BASE_DIR_CATALOGOS


def main():
    """Menú principal del programa Catálogo de Películas"""
    while True:
        print("\n🎬 === MENÚ PRINCIPAL ===")
        print("1) Crear catálogo nuevo")
        print("2) Ver catálogos existentes")
        print("3) Trabajar con un catálogo")
        print("4) Eliminar un catálogo")
        print("5) Salir")

        op = input("\nElegí una opción: ").strip()

        if op == "1":
            nombre = input("📁 Nombre del nuevo catálogo: ").strip()
            if not nombre:
                print("⚠️ El nombre no puede estar vacío.")
                continue
            catalogo = CatalogoPeliculas(nombre)
            print(f"✅ Catálogo '{nombre}' creado en {catalogo.ruta_archivo}")

        elif op == "2":
            mostrar_catalogos()

        elif op == "3":
            nombre = input("📂 Ingresá el nombre del catálogo existente: ").strip()
            if not nombre:
                print("⚠️ El nombre no puede estar vacío.")
                continue
            catalogo = CatalogoPeliculas(nombre)
            submenu_catalogo(catalogo)

        elif op == "4":
            eliminar_catalogo()

        elif op == "5":
            print("👋 ¡Gracias por usar el Catálogo de Películas!")
            break
        else:
            print("⚠️ Opción inválida. Intentá nuevamente.")


def mostrar_catalogos():
    """Muestra los catálogos disponibles"""
    if not os.path.exists(BASE_DIR_CATALOGOS):
        print("📂 No hay catálogos creados todavía.")
        return

    archivos = [f for f in os.listdir(BASE_DIR_CATALOGOS) if f.endswith(".txt")]
    if not archivos:
        print("📂 No hay catálogos creados todavía.")
        return

    print("\n📁 Catálogos disponibles:")
    for i, a in enumerate(archivos, start=1):
        print(f"  {i}. {a[:-4]}")


def eliminar_catalogo():
    """Elimina un catálogo existente"""
    mostrar_catalogos()
    nombre = input("\n📁 Nombre del catálogo a eliminar: ").strip()
    if not nombre:
        print("⚠️ El nombre no puede estar vacío.")
        return

    path = os.path.join(BASE_DIR_CATALOGOS, f"{nombre}.txt")
    if os.path.exists(path):
        confirm = input(f"¿Seguro que querés eliminar '{nombre}'? (s/n): ").strip().lower()
        if confirm == "s":
            os.remove(path)
            print("🗑️ Catálogo eliminado correctamente.")
        else:
            print("❌ Operación cancelada.")
    else:
        print("⚠️ Ese catálogo no existe.")


def submenu_catalogo(catalogo: CatalogoPeliculas):
    """Submenú para trabajar con un catálogo específico"""
    while True:
        print(f"\n🎞️ === Catálogo activo: {catalogo.nombre} ===")
        print("1) Agregar película")
        print("2) Listar películas")
        print("3) Eliminar película")
        print("4) Volver al menú principal")

        sub_op = input("\nElegí una opción: ").strip()

        # ---------- Agregar película ----------
        if sub_op == "1":
            titulo = input("🎥 Ingresá el nombre de la película: ").strip()
            if not titulo:
                print("⚠️ El título no puede estar vacío.")
                continue

            # El género se toma del nombre del catálogo
            genero_derive = normalizar_espacios(catalogo.nombre).capitalize()

            anio_str = input("📅 Año de estreno (opcional, Enter para omitir): ").strip()
            anio = 0
            if anio_str:
                try:
                    anio = int(anio_str)
                except ValueError:
                    print("⚠️ Año inválido. Se guardará sin año.")
                    anio = 0

            try:
                peli = Pelicula(titulo, genero_derive, anio)
                if catalogo.agregar(peli):
                    print(f"✅ '{peli}' agregada correctamente.")
                else:
                    print("⚠️ Esa película ya existe en el catálogo.")
            except ValueError as e:
                print(f"⚠️ {e}")

        # ---------- Listar películas ----------
        elif sub_op == "2":
            peliculas = catalogo.listar()
            if not peliculas:
                print("📂 El catálogo está vacío.")
            else:
                print("\n🎬 Películas:")
                for p in peliculas:
                    print(f"  - {p}")

        # ---------- Eliminar película ----------
        elif sub_op == "3":
            peliculas = catalogo.listar()
            if not peliculas:
                print("📂 El catálogo está vacío.")
                continue

            print("\n🎞️ Películas disponibles:")
            for i, p in enumerate(peliculas, start=1):
                print(f"  {i}. {p}")

            idx_str = input("\n🗑️ Ingresá el número de la película a eliminar: ").strip()
            if not idx_str.isdigit():
                print("⚠️ Valor inválido.")
                continue

            idx = int(idx_str)
            if not (1 <= idx <= len(peliculas)):
                print("⚠️ Número fuera de rango.")
                continue

            peli = peliculas[idx - 1]
            catalogo.eliminar(peli)
            print(f"🗑️ '{peli}' eliminada correctamente.")

        elif sub_op == "4":
            print("↩️ Volviendo al menú principal...")
            break
        else:
            print("⚠️ Opción inválida.")


if __name__ == "__main__":
    main()
