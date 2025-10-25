# gui_flet.py
import os
import flet as ft
from pelicula import Pelicula
from catalogo_peliculas import CatalogoPeliculas
from utils import BASE_DIR_CATALOGOS, normalizar_espacios


# ---------- helpers ----------
def listar_catalogos() -> list[str]:
    if not os.path.exists(BASE_DIR_CATALOGOS):
        os.makedirs(BASE_DIR_CATALOGOS, exist_ok=True)
        return []
    return sorted(
        [f[:-4] for f in os.listdir(BASE_DIR_CATALOGOS) if f.endswith(".txt")],
        key=str.lower,
    )


def ruta_catalogo(nombre: str) -> str:
    return os.path.join(BASE_DIR_CATALOGOS, f"{nombre}.txt")


def reescribir_catalogo(catalogo: CatalogoPeliculas, peliculas: list[Pelicula]) -> None:
    with open(catalogo.ruta_archivo, "w", encoding="utf-8") as f:
        for p in peliculas:
            f.write(p.to_line() + "\n")


# ---------- app ----------
def main(page: ft.Page):
    page.title = "Catálogo de Películas — So + Thel + Yami"
    page.window_width = 980
    page.window_height = 680
    page.padding = 16
    page.scroll = "auto"

    # Estado
    catalogos = listar_catalogos()

    catalogo_sel = ft.Dropdown(
        label="Catálogo",
        hint_text="Elegí un catálogo…",
        options=[ft.dropdown.Option(c) for c in catalogos],
        width=320,
    )
    btn_refrescar = ft.IconButton(icon="refresh")

    nuevo_catalogo = ft.TextField(label="Nuevo catálogo", width=260)
    btn_crear_catalogo = ft.ElevatedButton("Crear catálogo", icon="add")

    tf_nombre = ft.TextField(label="Título", expand=True)
    tf_anio = ft.TextField(label="Año (opcional)", width=150)
    btn_agregar = ft.FilledButton("Agregar", icon="movie")

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("#")),
            ft.DataColumn(ft.Text("Título")),
            ft.DataColumn(ft.Text("Género")),
            ft.DataColumn(ft.Text("Año")),
        ],
        rows=[],
        column_spacing=24,
        heading_row_height=40,
        data_row_min_height=36,
        show_checkbox_column=True,
    )

    btn_eliminar_sel = ft.OutlinedButton("Eliminar seleccionadas", icon="delete_outline")
    info_catalogo = ft.Text("", size=12, color="#777777")  # color manual en vez de ft.colors.GREY

    # Snackbar helper
    def toast(msg: str, ok: bool = True):
        bg = "#B9F6CA" if ok else "#FF8A80"  # verde claro / rojo claro
        page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor=bg, show_close_icon=True)
        page.snack_bar.open = True
        page.update()

    # Carga tabla
    def cargar_tabla(nombre_cat: str):
        if not nombre_cat:
            tabla.rows = []
            info_catalogo.value = "Sin catálogo seleccionado."
            page.update()
            return
        catalogo = CatalogoPeliculas(nombre_cat)
        pelis = catalogo.listar()
        tabla.rows = []
        for idx, p in enumerate(pelis, start=1):
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(idx))),
                        ft.DataCell(ft.Text(p.nombre)),
                        ft.DataCell(ft.Text(getattr(p, "genero", ""))),
                        ft.DataCell(ft.Text(str(getattr(p, "anio", "") or ""))),
                    ]
                )
            )
        info_catalogo.value = f"Archivo: {catalogo.ruta_archivo} — {len(pelis)} película(s)"
        page.update()

    # Eventos
    def on_refrescar(e):
        catalogo_sel.options = [ft.dropdown.Option(c) for c in listar_catalogos()]
        page.update()
        if catalogo_sel.value:
            cargar_tabla(catalogo_sel.value)

    def on_cambiar_catalogo(e):
        cargar_tabla(catalogo_sel.value)

    def on_crear_catalogo(e):
        nombre = normalizar_espacios(nuevo_catalogo.value or "")
        if not nombre:
            toast("El nombre del catálogo no puede estar vacío.", ok=False)
            return
        path = ruta_catalogo(nombre)
        if os.path.exists(path):
            toast("Ya existe un catálogo con ese nombre.", ok=False)
            return
        open(path, "w", encoding="utf-8").close()
        toast(f"Catálogo '{nombre}' creado.")
        catalogo_sel.options = [ft.dropdown.Option(c) for c in listar_catalogos()]
        catalogo_sel.value = nombre
        nuevo_catalogo.value = ""
        page.update()
        cargar_tabla(nombre)

    def on_agregar_pelicula(e):
        nombre = normalizar_espacios(tf_nombre.value or "")
        anio_str = (tf_anio.value or "").strip()
        anio = 0
        if anio_str:
            try:
                anio = int(anio_str)
            except ValueError:
                toast("Año inválido. Se guardará sin año.", ok=False)
                anio = 0

        if not catalogo_sel.value:
            toast("Elegí un catálogo primero.", ok=False)
            return
        if not nombre:
            toast("El título no puede estar vacío.", ok=False)
            return

        genero_derive = normalizar_espacios(catalogo_sel.value).capitalize()
        p = Pelicula(nombre, genero_derive, anio)
        catalogo = CatalogoPeliculas(catalogo_sel.value)
        if catalogo.agregar(p):
            toast(f"'{p.nombre}' agregada correctamente.")
            tf_nombre.value = ""
            tf_anio.value = ""
            page.update()
            cargar_tabla(catalogo_sel.value)
        else:
            toast("Esa película ya existe en el catálogo.", ok=False)

    def on_eliminar_seleccionadas(e):
        if not catalogo_sel.value:
            toast("Elegí un catálogo primero.", ok=False)
            return
        seleccion = []
        for row in tabla.rows:
            if row.selected:
                titulo = row.cells[1].content.value
                genero = row.cells[2].content.value
                anio = row.cells[3].content.value or "0"
                try:
                    anio = int(anio)
                except ValueError:
                    anio = 0
                seleccion.append(Pelicula(titulo, genero, anio))

        if not seleccion:
            toast("No hay filas seleccionadas.", ok=False)
            return

        catalogo = CatalogoPeliculas(catalogo_sel.value)
        actuales = catalogo.listar()
        restantes = [p for p in actuales if all(p.nombre != s.nombre for s in seleccion)]
        reescribir_catalogo(catalogo, restantes)
        toast(f"Eliminadas {len(seleccion)} película(s).")
        cargar_tabla(catalogo_sel.value)

    # Bindings
    btn_refrescar.on_click = on_refrescar
    catalogo_sel.on_change = on_cambiar_catalogo
    btn_crear_catalogo.on_click = on_crear_catalogo
    btn_agregar.on_click = on_agregar_pelicula
    btn_eliminar_sel.on_click = on_eliminar_seleccionadas

    # Layout
    page.add(
        ft.Column(
            spacing=16,
            controls=[
                ft.Row(
                    controls=[
                        catalogo_sel,
                        btn_refrescar,
                        ft.Container(width=16),
                        nuevo_catalogo,
                        btn_crear_catalogo,
                        ft.Container(width=16),
                        info_catalogo,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(),
                ft.Row(
                    controls=[tf_nombre, tf_anio, btn_agregar, btn_eliminar_sel],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=8),
                ft.Container(content=tabla, expand=True),
            ],
        )
    )

    if catalogos:
        catalogo_sel.value = catalogos[0]
        cargar_tabla(catalogos[0])
    page.update()


if __name__ == "__main__":
    ft.app(target=main)

