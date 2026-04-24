from playwright.sync_api import sync_playwright

def test_a11y_3():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("file:///app/Verticals/ridesDAO/RidesVertical_Complete_Spec.html")

        # Test theme toggle
        buttons = page.locator("button").all()
        for button in buttons:
            label = button.get_attribute("aria-label")
            print(f"Button text: '{button.inner_text()}', aria-label: '{label}', class: '{button.get_attribute('class')}'")

        browser.close()

if __name__ == "__main__":
    test_a11y_3()
