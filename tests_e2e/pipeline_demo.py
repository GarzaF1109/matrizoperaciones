"""Demo manual: abre UN solo navegador, corre todos los pasos como lo haria
una persona, y lo cierra hasta el final. No es un test de pytest -- es un
guion secuencial pensado para VERSE, no para integrarse a CI.

Uso:
    source venv/bin/activate
    python tests_e2e/pipeline_demo.py
"""
import os
import re
import time

from playwright.sync_api import sync_playwright, expect

CALCULADORA = os.getenv("CALCULADORA_URL", "http://localhost:8001")
VISOR = os.getenv("VISOR_URL", "http://localhost:8000/view")


def crear_matriz(page, nombre, datos):
    filas, cols = len(datos), len(datos[0])

    page.fill("#nombre", nombre)
    page.fill("#filas", str(filas))
    page.fill("#cols", str(cols))

    celdas = page.locator("#editorGrid input")
    for f in range(filas):
        for c in range(cols):
            celdas.nth(f * cols + c).fill(str(datos[f][c]))

    page.click("#btnGuardar")

    salida = page.locator("#outEditor")
    expect(salida).to_contain_text(nombre)
    id_ = int(re.search(r"id (\d+)", salida.inner_text()).group(1))
    expect(page.locator(f"#op1 option[value='{id_}']")).to_have_count(1)
    return id_


def paso(titulo):
    print(f"\n=== {titulo} ===")


def main():
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False, slow_mo=250)
        page = navegador.new_page()

        paso("Crear matriz y verla en el listado")
        page.goto(CALCULADORA)
        nombre_a = "Pipeline A"
        id1 = crear_matriz(page, nombre_a, [[1, 2], [3, 4]])
        expect(page.locator(".card", has_text=nombre_a)).to_be_visible()
        print(f"OK: matriz {nombre_a} creada con id {id1}")

        paso("Sumar dos matrices y verificar el resultado en pantalla")
        nombre_b = "Pipeline B"
        id2 = crear_matriz(page, nombre_b, [[5, 6], [7, 8]])
        page.select_option("#op1", value=str(id1))
        page.select_option("#op2", value=str(id2))
        page.get_by_role("button", name="Sumar", exact=True).click()
        resultado = page.locator("#outOperacion")
        expect(resultado).to_have_class(re.compile(r"\bok\b"))
        valores = resultado.locator(".view span").all_inner_texts()
        assert valores == ["6", "8", "10", "12"], valores
        print(f"OK: {nombre_a} + {nombre_b} = {valores}")

        paso("Multiplicar dos matrices y verificar el resultado")
        nombre_c = "Pipeline C"
        nombre_d = "Pipeline D"
        id3 = crear_matriz(page, nombre_c, [[1, 2, 3], [4, 5, 6]])
        id4 = crear_matriz(page, nombre_d, [[7, 8], [9, 10], [11, 12]])
        page.select_option("#op1", value=str(id3))
        page.select_option("#op2", value=str(id4))
        page.get_by_role("button", name="Multiplicar", exact=True).click()
        resultado = page.locator("#outOperacion")
        expect(resultado).to_have_class(re.compile(r"\bok\b"))
        valores = resultado.locator(".view span").all_inner_texts()
        assert valores == ["58", "64", "139", "154"], valores
        print(f"OK: {nombre_c} x {nombre_d} = {valores}")

        paso("Sumar matrices de distinta dimensión -> mensaje comprensible")
        nombre_e = "Pipeline E"
        id5 = crear_matriz(page, nombre_e, [[1, 2, 3], [4, 5, 6]])
        page.select_option("#op1", value=str(id1))
        page.select_option("#op2", value=str(id5))
        page.get_by_role("button", name="Sumar", exact=True).click()
        resultado = page.locator("#outOperacion")
        expect(resultado).to_have_class(re.compile(r"\berr\b"))
        expect(resultado).to_contain_text("misma dimensión")
        print(f"OK: mensaje de error legible -> {resultado.inner_text()}")

        paso("Determinante de una matriz conocida")
        nombre_f = "Pipeline Det"
        crear_matriz(page, nombre_f, [[2, 0], [0, 3]])
        tarjeta = page.locator(".card", has_text=nombre_f)
        tarjeta.get_by_role("button", name="Determinante").click()
        resultado = page.locator("#outUnitaria")
        expect(resultado).to_have_class(re.compile(r"\bok\b"))
        valor = resultado.locator(".big").inner_text()
        assert valor == "6", valor
        print(f"OK: determinante de {nombre_f} = {valor}")

        paso("Abrir el visor 3D y confirmar conexión")
        page.goto(VISOR)
        expect(page.get_by_text("Conectado", exact=True)).to_be_visible(timeout=5000)
        print("OK: visor conectado a la calculadora")

        print("\nTodo listo. Cerrando el navegador en 2 segundos...")
        time.sleep(2)
        navegador.close()


if __name__ == "__main__":
    main()
