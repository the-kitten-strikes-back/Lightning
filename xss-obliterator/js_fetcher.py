import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "xss-obliterator/1.0"
}

def fetch_js(url):
    scripts = []

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to fetch page: {e}")
        return scripts   # return EMPTY, not crash

    soup = BeautifulSoup(r.text, "html.parser")

    for script in soup.find_all("script"):
        # Inline JS
        if script.string:
            scripts.append(script.string)

        # External JS
        if script.get("src"):
            js_url = urljoin(url, script["src"])
            try:
                js = requests.get(js_url, headers=HEADERS, timeout=10).text
                scripts.append(js)
            except requests.exceptions.RequestException:
                print(f"[!] Skipping JS (timeout): {js_url}")
                continue

    return scripts
