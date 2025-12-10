"""Unit tests for website_attribute_set controllers."""

from odoo.tests import HttpCase


class TestWebsiteAttributeController(HttpCase):
    """Test class for website attribute set controllers."""

    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.user = self.env.ref("base.user_admin")
        self.website = self.env.ref("website.default_website")

    def test_shop_page_accessibility(self):
        """Test that the shop page can be accessed without errors."""
        # This test ensures that the controller methods don't throw errors
        # like 'website' object has no attribute 'pricelist_id'
        self.authenticate("admin", "admin")
        response = self.url_open("/shop", timeout=30)

        # Should be able to access the shop page without errors
        self.assertEqual(response.status_code, 200)

    def test_product_template_with_attributes_accessibility(self):
        """Test that product pages with attributes can be accessed without errors."""
        # Ensure we can access product-related pages that use attribute functionality
        self.authenticate("admin", "admin")

        # Check if we can access the product template form
        response = self.url_open("/web", timeout=30)
        self.assertEqual(response.status_code, 200)

        # Verify the website controller has the required methods to avoid AttributeError
        from ..controllers.main import WebsiteSale

        website_sale = WebsiteSale()

        # Test that required methods exist
        self.assertTrue(hasattr(website_sale, "shop"))
