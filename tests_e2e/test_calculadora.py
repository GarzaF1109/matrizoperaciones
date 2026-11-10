import re
import uuid

from playwright.sync_api import Page, expect


def nombre_unico(base: str) -> str:
    """El backend guarda las matrices en memoria entre corridas, así que cada
    prueba usa un nombre único para no chocar con datos de ejecuciones previas."""
    return f"{base} {uuid.uuid4().hex[:6]}"


def crear_matriz(page: Page, nombre: str, datos: list[list[float]]) -> int:
    """Llena el formulario de creación y devuelve el id asignado."""
    filas, cols = len(datos), len(datos[0])

    page.fill("#nombre", nombre)
    page.fill("#filas", str(filas))
    page.fill("#cols", str(cols))

    celdas = page.locator("#editorGrid input")
    for f in range(filas):
        for c in range(cols):
            celdas.nth(f * cols + c).fill(str(datos[f][c]))

    page.click("#btnGuardar")

    # Esperamos el NOMBRE (único por llamada), no solo "id \d+": ese patrón ya
    # lo satisfacía el mensaje de la creación anterior, así que no servía para
    # detectar que esta creación en particular ya terminó.
    salida = page.locator("#outEditor")
    expect(salida).to_contain_text(nombre)
    id_ = int(re.search(r"id (\d+)", salida.inner_text()).group(1))

    # guardar() recarga el listado (y los <select>) de forma asíncrona después
    # de mostrar el mensaje; esperamos a que la opción exista para no pisarla
    # con una selección hecha antes de que termine de recargar.
    expect(page.locator(f"#op1 option[value='{id_}']")).to_have_count(1)
    return id_


def test_crear_matriz_aparece_en_listado(page: Page, calculadora_url: str):
    page.goto(calculadora_url)

    nombre = nombre_unico("Matriz Test A")
    crear_matriz(page, nombre, [[1, 2], [3, 4]])

    tarjeta = page.locator(".card", has_text=nombre)
    expect(tarjeta).to_be_visible()
    expect(tarjeta).to_contain_text("2×2")


def test_sumar_dos_matrices_muestra_resultado(page: Page, calculadora_url: str):
    page.goto(calculadora_url)

    id1 = crear_matriz(page, nombre_unico("Suma A"), [[1, 2], [3, 4]])
    id2 = crear_matriz(page, nombre_unico("Suma B"), [[5, 6], [7, 8]])

    page.select_option("#op1", value=str(id1))
    page.select_option("#op2", value=str(id2))
    page.get_by_role("button", name="Sumar", exact=True).click()

    resultado = page.locator("#outOperacion")
    expect(resultado).to_have_class(re.compile(r"\bok\b"))
    expect(resultado).to_contain_text("2×2")

    valores = resultado.locator(".view span").all_inner_texts()
    assert valores == ["6", "8", "10", "12"]


def test_multiplicar_dos_matrices_muestra_resultado(page: Page, calculadora_url: str):
    page.goto(calculadora_url)

    id1 = crear_matriz(page, nombre_unico("Mult A"), [[1, 2, 3], [4, 5, 6]])
    id2 = crear_matriz(page, nombre_unico("Mult B"), [[7, 8], [9, 10], [11, 12]])

    page.select_option("#op1", value=str(id1))
    page.select_option("#op2", value=str(id2))
    page.get_by_role("button", name="Multiplicar", exact=True).click()

    resultado = page.locator("#outOperacion")
    expect(resultado).to_have_class(re.compile(r"\bok\b"))
    expect(resultado).to_contain_text("2×2")

    valores = resultado.locator(".view span").all_inner_texts()
    assert valores == ["58", "64", "139", "154"]


def test_sumar_dimensiones_distintas_muestra_mensaje_comprensible(page: Page, calculadora_url: str):
    page.goto(calculadora_url)

    id1 = crear_matriz(page, nombre_unico("Dim A"), [[1, 2], [3, 4]])
    id2 = crear_matriz(page, nombre_unico("Dim B"), [[1, 2, 3], [4, 5, 6]])

    page.select_option("#op1", value=str(id1))
    page.select_option("#op2", value=str(id2))
    page.get_by_role("button", name="Sumar", exact=True).click()

    resultado = page.locator("#outOperacion")
    expect(resultado).to_have_class(re.compile(r"\berr\b"))
    expect(resultado).to_contain_text("misma dimensión")


def test_determinante_de_matriz_conocida(page: Page, calculadora_url: str):
    page.goto(calculadora_url)

    nombre = nombre_unico("Det Conocida")
    crear_matriz(page, nombre, [[2, 0], [0, 3]])

    tarjeta = page.locator(".card", has_text=nombre)
    tarjeta.get_by_role("button", name="Determinante").click()

    resultado = page.locator("#outUnitaria")
    expect(resultado).to_have_class(re.compile(r"\bok\b"))
    expect(resultado.locator(".big")).to_have_text("6")
