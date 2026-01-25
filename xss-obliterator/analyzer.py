SOURCES = [
    "location",
    "window.location",
    "document.location",
    "location.search",
    "location.hash",
    "URLSearchParams"
]

SINKS = [
    "innerHTML",
    "outerHTML",
    "document.write",
    "eval(",
    "setTimeout(",
    "setInterval(",
    "insertAdjacentHTML"
]

MAX_DISTANCE = 300  # characters

def analyze(js_code: str):
    findings = []

    for src in SOURCES:
        for sink in SINKS:
            src_index = js_code.find(src)
            sink_index = js_code.find(sink)

            if src_index != -1 and sink_index != -1:
                if abs(src_index - sink_index) <= MAX_DISTANCE:
                    findings.append((src, sink))

    return findings
