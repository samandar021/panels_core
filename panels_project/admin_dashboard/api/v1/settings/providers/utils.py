from urllib.parse import urlparse

from modules.utils.idn_convertation import DomainConverter


def validate_domain(domain: str) -> str:
    parsed = urlparse(domain)
    clean_domain = parsed.netloc or parsed.path
    clean_domain = clean_domain.split("//")[-1]
    clean_domain = clean_domain.split("/")[0]
    clean_domain = clean_domain.lower()
    if clean_domain.startswith("www."):
        clean_domain = clean_domain[4:]
    clean_domain = DomainConverter.to_punycode(clean_domain)
    return clean_domain
