from urllib.parse import urlparse


def extract_external_id(url: str, source_code: str) -> str | None:
    """Extract external id from url."""
    if source_code != "hh":
        return None

    parse_result = urlparse(url)
    hostname = parse_result.hostname

    if not hostname or hostname.lower() == "adsrv.hh.ru":
        return None

    parts = [p for p in parse_result.path.split("/") if p]

    if len(parts) >= 2 and parts[0] == "vacancy" and parts[1].isdigit():
        return parts[1]
    return None
