from playwright.sync_api import Page, expect

VISOR = "http://localhost:8000/view"


def test_visor_se_conecta(page: Page):          # pytest inyecta la página
    # Arrange: abrir la aplicación
    page.goto(VISOR)

    # Assert: esperar el estado (reintenta hasta 5 s)
    expect(page.get_by_text("Conectado", exact=True)).to_be_visible(timeout=5000)
