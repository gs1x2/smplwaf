import time
from playwright.sync_api import sync_playwright

def verify_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Login with admin credentials
        context = browser.new_context(http_credentials={"username": "admin", "password": "admin"})
        page = context.new_page()

        # Navigate to the dashboard
        page.goto("http://127.0.0.1:57230")
        page.wait_for_load_state("networkidle")

        # Switch to Rules view
        page.evaluate("switchView('rules')")
        time.sleep(1) # wait for render

        # Click the folder to expand
        folder = page.locator("span.folder").filter(has_text="global/")
        folder.click()
        time.sleep(1) # wait for animation

        # Hover over the file to reveal the delete button
        file_item = page.locator("li.file").filter(has_text="test.rule")
        file_item.hover()
        time.sleep(0.5) # wait for hover state

        # Take a screenshot
        page.screenshot(path="screenshot.png")
        print("Screenshot saved to screenshot.png")

        browser.close()

if __name__ == "__main__":
    verify_ui()
