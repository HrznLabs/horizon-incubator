from playwright.sync_api import sync_playwright

def test_a11y():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("file:///app/Verticals/ridesDAO/RidesVertical_Complete_Spec.html")

        # Look for missing ARIA labels or poor contrast
        buttons = page.locator("button").all()
        for button in buttons:
            label = button.get_attribute("aria-label")
            text = button.inner_text()
            if not label and not text.strip():
                print(f"Found button with no text or ARIA label: {button}")

        # Let's also check link focus styles and general DOM
        print("Page title:", page.title())

        browser.close()

if __name__ == "__main__":
    test_a11y()
