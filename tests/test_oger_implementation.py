"""Test OGERImplementation."""
import unittest

from oaklib.implementations import get_implementation_resolver
from oaklib.selector import get_resource_from_shorthand

from oakx_oger.oger_implementation import OGERImplementation
from tests import TEST_OWL


class TestOGERImplementation(unittest.TestCase):
    """Test OGERImplementation."""

    def test_plugin(self):
        """Tests plugins are discovered."""
        implementation_resolver = get_implementation_resolver()
        resolved = implementation_resolver.lookup("OGER")
        self.assertEqual(resolved, OGERImplementation)

        slug = f"oger:{TEST_OWL}"
        r = get_resource_from_shorthand(slug)
        self.assertEqual(r.implementation_class, OGERImplementation)
