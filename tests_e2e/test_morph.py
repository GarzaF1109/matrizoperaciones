import uuid

from playwright.sync_api import Page, expect


def test_slider_morph_arranca_en_dona(page: Page, visor_url: str):
    page.goto(visor_url)
    expect(page.get_by_text("Conectado", exact=True)).to_be_visible(timeout=5000)

    expect(page.locator("#morph")).to_have_value("0")
    expect(page.locator("#morphValor")).to_have_text("0.00")


def test_mover_el_slider_a_taza_no_muestra_error(page: Page, visor_url: str):
    page.goto(visor_url)
    expect(page.get_by_text("Conectado", exact=True)).to_be_visible(timeout=5000)

    slider = page.locator("#morph")
    slider.focus()
    page.keyboard.press("End")  # manda el slider al máximo (1 = taza)

    expect(page.locator("#morphValor")).to_have_text("1.00")
    # El morph tarda un roundtrip por la calculadora; damos tiempo y
    # verificamos que no haya quedado un mensaje de error en pantalla.
    page.wait_for_timeout(500)
    expect(page.locator("#estado.err")).to_have_count(0)


def test_guardar_figura_con_nombre_muestra_confirmacion(page: Page, visor_url: str):
    page.goto(visor_url)
    expect(page.get_by_text("Conectado", exact=True)).to_be_visible(timeout=5000)

    nombre = f"figura-{uuid.uuid4().hex[:6]}"
    page.fill("#nombreFigura", nombre)
    page.click("#guardarFigura")

    expect(page.locator("#figuraEstado")).to_contain_text(nombre, timeout=5000)
