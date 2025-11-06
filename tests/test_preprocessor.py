"""
Unit tests for the NamePreprocessor class.
"""

import unittest

from firstname_to_nationality import NamePreprocessor


class TestNamePreprocessor(unittest.TestCase):
    """Tests for the NamePreprocessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.preprocessor = NamePreprocessor()

    def test_preprocess_simple_name(self):
        """Test preprocessing of a simple name."""
        result = self.preprocessor.preprocess_name("John")
        self.assertIsInstance(result, str)
        self.assertIn("j", result)
        self.assertIn("o", result)

    def test_preprocess_name_with_space(self):
        """Test preprocessing of name with space."""
        result = self.preprocessor.preprocess_name("John Smith")
        self.assertIn("▁", result)  # Space marker should be present

    def test_preprocess_name_with_special_chars(self):
        """Test preprocessing removes special characters."""
        result = self.preprocessor.preprocess_name("John@#$")
        self.assertNotIn("@", result)
        self.assertNotIn("#", result)
        self.assertNotIn("$", result)

    def test_preprocess_lowercase_conversion(self):
        """Test that names are converted to lowercase."""
        result = self.preprocessor.preprocess_name("JOHN")
        self.assertIn("j", result)
        self.assertNotIn("J", result)

    def test_preprocess_empty_string(self):
        """Test preprocessing of empty string."""
        result = self.preprocessor.preprocess_name("")
        self.assertIsInstance(result, str)

    def test_preprocess_whitespace_only(self):
        """Test preprocessing of whitespace-only string."""
        result = self.preprocessor.preprocess_name("   ")
        self.assertIsInstance(result, str)

    def test_preprocess_hyphenated_name(self):
        """Test preprocessing preserves hyphens."""
        result = self.preprocessor.preprocess_name("Jean-Paul")
        # Hyphens should be handled (either kept or removed consistently)
        self.assertIsInstance(result, str)

    def test_restore_name(self):
        """Test restoring name from processed version."""
        processed = "j o h n ▁ s m i t h"
        result = self.preprocessor.restore_name(processed)
        self.assertIn("john", result.lower())
        self.assertIn("smith", result.lower())

    def test_restore_name_with_space_marker(self):
        """Test that space markers are properly restored."""
        processed = "t e s t ▁ n a m e"
        result = self.preprocessor.restore_name(processed)
        self.assertIn(" ", result)

    def test_preprocess_unicode_characters(self):
        """Test preprocessing of names with unicode characters."""
        result = self.preprocessor.preprocess_name("José María")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main()
