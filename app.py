# app.py
from catalogo_peliculas import CatalogoPeliculas
from pelicula import Pelicula

def pedir_opcion() -> str:
    print("\n===== MENÚ =====")
    print("1) Agregar película")
    print("2) Listar películas")
    print("3) Eliminar catálogo de películas")
    print("4) Salir")
    return input("Elegí una opción (1-4): ").strip()

def main():
    print("Bienvenid@ 👋")
    nombre_catalogo = input("Ingresá el nombre del catálogo de películas: ").strip()
    catalogo = CatalogoPeliculas(nombre_catalogo)

    # Si el archivo no existe, queda creado al primer 'agregar'.
    print(f"\nCatálogo seleccionado: '{catalogo.nombre}' -> {catalogo.ruta_archivo}")

    while True:
        opcion = pedir_opcion()

        if opcion == "1":
            titulo = input("Nombre de la película a agregar: ").strip()
            try:
                peli = Pelicula(titulo)
                catalogo.agregar(peli)
                print(f"✅ Película agregada: {peli}")
            except ValueError as e:
                print(f"⚠️ {e}")

        elif opcion == "2":
            peliculas = catalogo.listar()
            if not peliculas:
                print("📭 El catálogo está vacío (o todavía no existe el archivo).")
            else:
                print("\n🎬 Películas del catálogo:")
                for i, p in enumerate(peliculas, start=1):
                    print(f"  {i}. {p}")

        elif opcion == "3":
            conf = input("¿Seguro que querés eliminar el catálogo? (sí/no): ").strip().lower()
            if conf in ("si", "sí", "s"):
                if catalogo.eliminar_catalogo():
                    print("🗑️ Catálogo eliminado.")
                else:
                    print("ℹ️ El catálogo no existía.")
            else:
                print("↩️ Cancelado.")

        elif opcion == "4":
            print("👋 ¡Gracias por usar el gestor de películas! Programa finalizado.")
            break

        else:
            print("❌ Opción inválida. Elegí 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()
