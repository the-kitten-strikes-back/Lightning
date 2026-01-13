import argparse
from banner import show_banner
from js_fetcher import fetch_js
from analyzer import analyze
from verifier import verify_dom_xss

HELP_EPILOG = """
Tags explained:
  [DOM-XSS]        Potential DOM-based XSS source → sink flow
  [🔥] EXPLOITABLE  XSS payload executed successfully
  [⚠️] POSSIBLE     Dangerous pattern found, execution not confirmed
  [i] INFO         Informational message
  [!] WARNING      Partial failure (timeouts, blocked fetches)

Examples:
  python main.py -u https://example.com
  python main.py -u http://localhost:3000/#/search --verify
"""

def main():
    show_banner()

    parser = argparse.ArgumentParser(
        description="xss-obliterator — DOM XSS recon + exploit verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=HELP_EPILOG
    )

    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("--verify", action="store_true", help="Verify exploitability")

    args = parser.parse_args()

    print(f"[+] Scanning {args.url}")

    scripts = fetch_js(args.url)
    print(f"[+] JavaScript blocks found: {len(scripts)}")

    if not scripts:
        print("[i] INFO — no JavaScript found to analyze.")
        return

    findings = set()

    for js in scripts:
        for src, sink in analyze(js):
            findings.add((src, sink))

    if not findings:
        print("[i] INFO — no obvious DOM XSS patterns found.")
        return

    print("\n[!] Potential DOM XSS patterns detected:")
    for src, sink in findings:
        print(f"    [DOM-XSS] {src} → {sink}")

    if args.verify:
        print("\n[*] Verifying exploitability in real browser...")
        exploitable = verify_dom_xss(args.url)

        if exploitable:
            print("[🔥] EXPLOITABLE — DOM XSS confirmed")
        else:
            print("[⚠️] POSSIBLE — dangerous patterns found, execution not confirmed")
            print("    Manual testing recommended.")
    else:
        print("\n[i] INFO — use --verify to attempt runtime confirmation")

    print("\n[✓] Scan completed.")

if __name__ == "__main__":
    main()
