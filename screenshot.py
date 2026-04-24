from playwright.sync_api import sync_playwright

def screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("file:///app/Verticals/ridesDAO/RidesVertical_Complete_Spec.html")
        page.wait_for_timeout(2000)
        page.screenshot(path="screenshot.png", full_page=True)
        browser.close()

if __name__ == "__main__":
    screenshot()
