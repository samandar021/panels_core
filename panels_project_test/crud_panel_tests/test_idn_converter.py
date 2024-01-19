import unittest

from modules.utils.idn_convertation import DomainConverter


class TestDomainConverter(unittest.TestCase):

    def test_to_punycode(self):
        # Тест корректного домена
        self.assertEqual(DomainConverter.to_punycode("example.com"), "example.com")

        # Тест домена с символами Unicode
        self.assertEqual(DomainConverter.to_punycode("привет.дед"), "xn--b1agh1afp.xn--d1aac")

        # Тест невалидного домена
        self.assertIsInstance(DomainConverter.to_punycode("-example"), str)

    def test_from_punycode(self):
        # Тест корректного домена
        self.assertEqual(DomainConverter.from_punycode("example.com"), "example.com")

        # Тест домена с символами Punycode
        self.assertEqual(DomainConverter.from_punycode("xn--b1agh1afp.xn--d1aac"), "привет.дед")

        # Тест невалидного домена
        self.assertIsInstance(DomainConverter.from_punycode("-example"), str)
