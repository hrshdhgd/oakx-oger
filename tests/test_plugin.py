"""Test OGERImplementation."""
import unittest

from oaklib.implementations import get_implementation_resolver
from oaklib.selector import get_resource_from_shorthand

from tests import TEST_OWL


class TestPlugin(unittest.TestCase):
    """Test OGERImplementation."""

    def test_plugin(self):
        """Tests plugins are discovered."""
        # This needs to be imported here to avoid circular imports
        from oakx_oger.oger_implementation import OGERImplementation

        implementation_resolver = get_implementation_resolver()
        resolved = implementation_resolver.lookup("oger")
        self.assertEqual(resolved, OGERImplementation)

        slug = f"oger:{TEST_OWL}"
        r = get_resource_from_shorthand(slug)
        self.assertEqual(r.implementation_class, OGERImplementation)
