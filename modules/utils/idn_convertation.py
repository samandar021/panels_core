class DomainConverter:
    @staticmethod
    def to_punycode(domain: str) -> str:
        try:
            return domain.encode('idna').decode('utf-8')
        except Exception as e:
            return str(e)

    @staticmethod
    def from_punycode(punycode: str) -> str:
        try:
            return punycode.encode('idna').decode('idna')
        except Exception as e:
            return str(e)
