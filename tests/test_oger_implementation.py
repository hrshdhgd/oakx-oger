from tests import TEST_OWL

import unittest

from oaklib.selector import get_resource_from_shorthand
from oaklib.implementations import get_implementation_resolver
from oakx_oger.oger_implementation import OGERImplementation

class TestOGERImplementation(unittest.TestCase):
    """Test OGERImplementation."""
        
    def test_plugin(self):
        """tests plugins are discovered"""
        implementation_resolver = get_implementation_resolver()
        resolved = implementation_resolver.lookup("FOO")
        self.assertEqual(resolved, OGERImplementation)

        slug = f"oger:{TEST_OWL}"
        r = get_resource_from_shorthand(slug)
        self.assertEqual(r.implementation_class, OGERImplementation)
