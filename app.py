# app.py
import os
from catalogo_peliculas import CatalogoPeliculas
from pelicula import Pelicula
from utils import BASE_DIR_CATALOGOS


# ======= MENÚS =======

def menu_principal():
    print("\n🎬 === MENÚ PRINCIPAL ===")
    print("1) Crear catálogo nuevo")
    print("2) Ver catálogos existentes")
    print("3) Trabajar con un catálogo")
    print("4) Eliminar un catálogo")
    print("5) Salir del programa")
    return input("Elegí una opción (1-5): ").strip()


def menu_catalogo(nombre):
    print(f"\n📁 === Catálogo activo: {nombre} ===")
    print("1) Agregar película")
    print("2) Listar películas")
    print("3) Eliminar película")
    print("4) Volver al menú principal")
    return input("Elegí una opción (1-4): ").strip()


def obtener_catalogos_existentes():
    """Devuelve una lista con los nombres de los catálogos .txt existentes."""
    if not os.path.exists(BASE_DIR_CATALOGOS):
        return []
    archivos = [
        f.replace(".txt", "")
        for f in os.listdir(BASE_DIR_CATALOGOS)
        if f.endswith(".txt")
    ]
    return archivos


# ======= PROGRAMA PRINCIPAL =======

def main():
    print("🎞️ Bienvenid@ al Gestor de Catálogos de Películas 🎞️")

    while True:
        opcion = menu_principal()

        # 1️⃣ Crear nuevo catálogo
        if opcion == "1":
            nombre = input("🆕 Ingresá el nombre del nuevo catálogo: ").strip()
            if not nombre:
                print("⚠️ El nombre no puede estar vacío.")
                continue
            ruta = os.path.join(BASE_DIR_CATALOGOS, f"{nombre}.txt")
            if os.path.exists(ruta):
                print("⚠️ Ya existe un catálogo con ese nombre.")
            else:
                open(ruta, "w", encoding="utf-8").close()
                print(f"✅ Catálogo '{nombre}' creado correctamente.")

        # 2️⃣ Ver catálogos existentes
        elif opcion == "2":
            catalogos = obtener_catalogos_existentes()
            if not catalogos:
                print("📭 No hay catálogos creados aún.")
            else:
                print("\n📚 Catálogos disponibles:")
                for i, cat in enumerate(catalogos, start=1):
                    print(f"  {i}. {cat}")

        # 3️⃣ Trabajar con un catálogo
        elif opcion == "3":
            catalogos = obtener_catalogos_existentes()
            if not catalogos:
                print("⚠️ No hay catálogos disponibles. Creá uno primero.")
                continue

            print("\n📚 Catálogos existentes:")
            for i, cat in enumerate(catalogos, start=1):
                print(f"  {i}. {cat}")
            try:
                idx = int(input("Seleccioná un número de catálogo: "))
                nombre_sel = catalogos[idx - 1]
            except (ValueError, IndexError):
                print("⚠️ Opción inválida.")
                continue

            catalogo = CatalogoPeliculas(nombre_sel)
            print(f"\n📂 Trabajando en el catálogo: '{catalogo.nombre}'")

            # === SUBMENÚ DE CATÁLOGO ===
            while True:
                sub_op = menu_catalogo(catalogo.nombre)

                # Agregar película
                if sub_op == "1":
                    titulo = input("🎥 Ingresá el nombre de la película: ").strip()
                    try:
                        peli = Pelicula(titulo)
                        if catalogo.agregar(peli):
                            print(f"✅ '{peli}' agregada correctamente.")
                        else:
                            print("⚠️ Esa película ya existe en el catálogo.")
                    except ValueError as e:
                        print(f"⚠️ {e}")

                # Listar películas
                elif sub_op == "2":
                    peliculas = catalogo.listar()
                    if not peliculas:
                        print("📭 El catálogo está vacío.")
                    else:
                        print(f"\n🎬 Películas en '{catalogo.nombre}':")
                        for i, p in enumerate(peliculas, start=1):
                            print(f"  {i}. {p}")

                # Eliminar película
                elif sub_op == "3":
                    peliculas = catalogo.listar()
                    if not peliculas:
                        print("📭 El catálogo está vacío, no hay nada para eliminar.")
                        continue

                    print(f"\n🎬 Películas en '{catalogo.nombre}':")
                    for i, p in enumerate(peliculas, start=1):
                        print(f"  {i}. {p}")

                    try:
                        idx = int(input("Seleccioná el número de la película a eliminar: "))
                        peli_sel = peliculas[idx - 1]
                    except (ValueError, IndexError):
                        print("⚠️ Opción inválida.")
                        continue

                    confirm = input(f"¿Seguro que querés eliminar '{peli_sel}'? (sí/no): ").strip().lower()
                    if confirm in ("si", "sí", "s"):
                        # Reescribimos el archivo sin la película seleccionada
                        nuevas = [p for p in peliculas if p.nombre != peli_sel.nombre]
                        with open(catalogo.ruta_archivo, "w", encoding="utf-8") as f:
                            for p in nuevas:
                                f.write(p.to_line() + "\n")
                        print(f"🗑️ '{peli_sel}' eliminada correctamente del catálogo.")
                    else:
                        print("↩️ Cancelado.")

                # Volver al menú principal
                elif sub_op == "4":
                    print(f"↩️ Volviendo al menú principal desde '{catalogo.nombre}'.")
                    break

                else:
                    print("❌ Opción inválida.")

        # 4️⃣ Eliminar un catálogo
        elif opcion == "4":
            catalogos = obtener_catalogos_existentes()
            if not catalogos:
                print("📭 No hay catálogos para eliminar.")
                continue

            print("\n📚 Catálogos existentes:")
            for i, cat in enumerate(catalogos, start=1):
                print(f"  {i}. {cat}")
            try:
                idx = int(input("Seleccioná un número de catálogo a eliminar: "))
                nombre_sel = catalogos[idx - 1]
            except (ValueError, IndexError):
                print("⚠️ Opción inválida.")
                continue

            confirm = input(f"¿Seguro que querés eliminar '{nombre_sel}'? (sí/no): ").strip().lower()
            if confirm in ("si", "sí", "s"):
                ruta = os.path.join(BASE_DIR_CATALOGOS, f"{nombre_sel}.txt")
                if os.path.exists(ruta):
                    os.remove(ruta)
                    print(f"🗑️ Catálogo '{nombre_sel}' eliminado.")
                else:
                    print("⚠️ El archivo no existe.")
            else:
                print("↩️ Cancelado.")

        # 5️⃣ Salir del programa
        elif opcion == "5":
            print("👋 ¡Gracias por usar el Gestor de Catálogos de Películas! Hasta pronto.")
            break

        else:
            print("❌ Opción inválida. Elegí entre 1 y 5.")


if __name__ == "__main__":
    main()
