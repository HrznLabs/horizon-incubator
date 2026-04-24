from playwright.sync_api import sync_playwright

def test_a11y_2():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("file:///app/Verticals/ridesDAO/RidesVertical_Complete_Spec.html")

        # Test keyboard nav by pressing Tab repeatedly
        for _ in range(5):
            page.keyboard.press("Tab")
            page.wait_for_timeout(100)

        print("Done")

        browser.close()

if __name__ == "__main__":
    test_a11y_2()
