from playwright.sync_api import sync_playwright
import time

def test_a11y_3():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        page.goto("file:///app/Verticals/ridesDAO/RidesVertical_Complete_Spec.html")

        page.evaluate("window.scrollBy(0, 5000)")
        time.sleep(2)

        btn = page.locator("#back-to-top")
        btn.hover()
        time.sleep(2)

        page.screenshot(path="full_page_hover.png")

        browser.close()

if __name__ == "__main__":
    test_a11y_3()
