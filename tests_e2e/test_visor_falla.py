import subprocess
from pathlib import Path

from playwright.sync_api import Page, expect

PROYECTO = Path(__file__).resolve().parent.parent


def test_visor_se_conecta(page: Page, visor_url: str):
    page.goto(visor_url)
    expect(page.get_by_text("Conectado", exact=True)).to_be_visible(timeout=5000)


def test_visor_muestra_error_si_calculadora_no_responde(page: Page, visor_url: str):
    page.goto(visor_url)
    expect(page.get_by_text("Conectado", exact=True)).to_be_visible(timeout=5000)

    subprocess.run(["docker", "compose", "stop", "calculadora"], cwd=PROYECTO, check=True)
    try:
        # Cambiamos "puntos" a un valor que el visor todavía no calculó, para
        # forzar una llamada real a la calculadora (si reusara el caché del
        # valor por defecto, no se notaría que está caída).
        slider = page.locator("#puntos")
        slider.focus()
        page.keyboard.press("End")  # manda el slider al máximo (4000)

        expect(page.get_by_text("calculadora no disponible", exact=True)).to_be_visible(timeout=5000)
    finally:
        subprocess.run(["docker", "compose", "start", "calculadora"], cwd=PROYECTO, check=True)
