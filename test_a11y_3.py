from playwright.sync_api import sync_playwright

def test_a11y_3():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("file:///app/Verticals/ridesDAO/RidesVertical_Complete_Spec.html")

        page.wait_for_timeout(1000)
        page.screenshot(path="full_page.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    test_a11y_3()
