import re
from service_db import SERVICE_DB
from probes import grab_banner, http_probe, smb_probe

def detect_service(target, port):
    if port not in SERVICE_DB:
        return None

    service_info = SERVICE_DB[port]
    response = ""

    if service_info["service"] in ["http", "https"]:
        response = http_probe(target, port)
    elif service_info["service"] in ["smb"]:
        response = smb_probe(target,port)
        if port == 445:
            info = smb_probe(target, port)
            if info:
                product = "SMB"
                version = None
                confidence = 70

                os_info = info.get("server_os", "")
                dialect = info.get("dialect")

                if "Samba" in os_info or "Unix" in os_info or "Linux" in os_info:
                    product = "Samba"
                    confidence = 90
                elif "Windows" in os_info:
                    product = "Windows SMB"
                    confidence = 90

                if dialect:
                    version = f"{dialect}"

                return {
                    "service": "smb",
                    "product": product,
                    "version": version,
                    "confidence": confidence,
                }

    else:
        response = grab_banner(target, port)

    response_lower = response.lower()

    best_match = {
        "service": service_info["service"],
        "product": "unknown",
        "version": None,
        "confidence": 0
    }

    for product, fp in service_info["fingerprints"].items():
        for pattern in fp["patterns"]:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                version = match.group(1) if match.groups() else None
                score = fp["score"]

                if score > best_match["confidence"]:
                    best_match.update({
                        "product": product,
                        "version": version,
                        "confidence": score
                    })

    return best_match
