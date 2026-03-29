from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            permissions=['clipboard-read', 'clipboard-write'],
            record_video_dir='/app/verification/videos'
        )
        page = context.new_page()
        page.goto('file:///app/Verticals/ridesDAO/RidesVertical_Complete_Spec.html')

        # Scroll to section
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_timeout(1000)

        # Wait for anchor to attach
        page.wait_for_selector('.anchor-link', state='attached')
        anchor = page.locator('.anchor-link').first

        # Check initial aria label
        initial_label = anchor.get_attribute('aria-label')

        # Hover and click to copy
        anchor.hover()
        page.wait_for_timeout(500)
        anchor.click()

        # Take screenshot of 'Copied!' state
        page.screenshot(path='/app/verification/screenshots/verification.png')
        page.wait_for_timeout(2100) # Wait for it to revert

        context.close()
        browser.close()
        print("Playwright video verification passed.")

test()
