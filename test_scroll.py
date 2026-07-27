from playwright.sync_api import sync_playwright

def test_scroll():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("file:///app/Verticals/ridesDAO/RidesVertical_Complete_Spec.html")

        # Scroll to a mermaid diagram and scroll it horizontally to show scrollbar
        page.evaluate("window.scrollTo(0, document.querySelector('.mermaid').offsetTop - 100);")
        page.evaluate("document.querySelector('.mermaid').scrollLeft = 50;")

        page.wait_for_timeout(1000)
        page.screenshot(path="mermaid_scrollbar.png")

        browser.close()

if __name__ == "__main__":
    test_scroll()
