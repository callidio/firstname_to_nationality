"""
Tests for setup_utils module.

Tests the utility functions used by setup.py for parsing requirements
and filtering packages.
"""

from setup_utils import (
    _extract_package_name,
    exclude_packages_by_name,
    filter_packages_by_name,
    read_requirements,
)


class TestExtractPackageName:
    """Tests for _extract_package_name helper function."""

    def test_extract_with_equal_equal(self):
        """Test extraction with == specifier."""
        assert _extract_package_name("numpy==1.0.0") == "numpy"

    def test_extract_with_greater_equal(self):
        """Test extraction with >= specifier."""
        assert _extract_package_name("pandas>=2.0.0") == "pandas"

    def test_extract_with_less_equal(self):
        """Test extraction with <= specifier."""
        assert _extract_package_name("matplotlib<=3.0.0") == "matplotlib"

    def test_extract_with_greater(self):
        """Test extraction with > specifier."""
        assert _extract_package_name("scipy>1.0") == "scipy"

    def test_extract_with_less(self):
        """Test extraction with < specifier."""
        assert _extract_package_name("scikit-learn<2.0") == "scikit-learn"

    def test_extract_with_not_equal(self):
        """Test extraction with != specifier."""
        assert _extract_package_name("joblib!=1.0.0") == "joblib"

    def test_extract_with_tilde_equal(self):
        """Test extraction with ~= specifier."""
        assert _extract_package_name("requests~=2.0") == "requests"

    def test_extract_with_triple_equal(self):
        """Test extraction with === specifier."""
        assert _extract_package_name("package===1.0.0") == "package"

    def test_extract_with_hyphen_in_name(self):
        """Test extraction with hyphenated package name."""
        assert _extract_package_name("scikit-learn==1.0.0") == "scikit-learn"

    def test_extract_with_underscore_in_name(self):
        """Test extraction with underscored package name."""
        assert _extract_package_name("some_package==1.0.0") == "some_package"

    def test_extract_no_version_specifier(self):
        """Test extraction with no version specifier."""
        assert _extract_package_name("numpy") == "numpy"


class TestReadRequirements:
    """Tests for read_requirements function."""

    def test_read_simple_requirements(self, tmp_path):
        """Test reading a simple requirements file."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("numpy==1.0.0\npandas==2.0.0\n")

        result = read_requirements("requirements.txt", base_path=tmp_path)
        assert result == ["numpy==1.0.0", "pandas==2.0.0"]

    def test_read_requirements_with_comments(self, tmp_path):
        """Test reading requirements file with comments."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text(
            "# This is a comment\n"
            "numpy==1.0.0\n"
            "# Another comment\n"
            "pandas==2.0.0\n"
        )

        result = read_requirements("requirements.txt", base_path=tmp_path)
        assert result == ["numpy==1.0.0", "pandas==2.0.0"]

    def test_read_requirements_with_inline_comments(self, tmp_path):
        """Test reading requirements file with inline comments."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text(
            "numpy==1.0.0  # inline comment\n"
            "pandas==2.0.0 # another inline comment\n"
        )

        result = read_requirements("requirements.txt", base_path=tmp_path)
        assert result == ["numpy==1.0.0", "pandas==2.0.0"]

    def test_read_requirements_with_line_continuations(self, tmp_path):
        """Test reading requirements file with line continuations."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text(
            "numpy==1.0.0\n" "pandas==2.0.0 \\\n" "  --hash=sha256:abc123\n"
        )

        result = read_requirements("requirements.txt", base_path=tmp_path)
        # Line continuation should combine lines
        assert len(result) == 2
        assert "numpy==1.0.0" in result
        assert "pandas==2.0.0" in result[1]
        assert "--hash=sha256:abc123" in result[1]

    def test_read_requirements_with_empty_lines(self, tmp_path):
        """Test reading requirements file with empty lines."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("numpy==1.0.0\n" "\n" "pandas==2.0.0\n" "\n")

        result = read_requirements("requirements.txt", base_path=tmp_path)
        assert result == ["numpy==1.0.0", "pandas==2.0.0"]

    def test_read_nonexistent_file(self, tmp_path):
        """Test reading a file that doesn't exist."""
        result = read_requirements("nonexistent.txt", base_path=tmp_path)
        assert result == []


class TestFilterPackagesByName:
    """Tests for filter_packages_by_name function."""

    def test_filter_exact_match(self):
        """Test filtering with exact package name match."""
        requirements = ["numpy==1.0.0", "pandas==2.0.0", "matplotlib==3.0.0"]
        package_names = {"numpy", "pandas"}
        result = filter_packages_by_name(requirements, package_names)
        assert set(result) == {"numpy==1.0.0", "pandas==2.0.0"}

    def test_filter_different_version_specifiers(self):
        """Test filtering with different version specifiers."""
        requirements = [
            "numpy==1.0.0",
            "pandas>=2.0.0",
            "matplotlib<=3.0.0",
            "scipy>1.0",
            "scikit-learn<2.0",
            "joblib!=1.0.0",
        ]
        package_names = {"numpy", "matplotlib", "joblib"}
        result = filter_packages_by_name(requirements, package_names)
        assert set(result) == {"numpy==1.0.0", "matplotlib<=3.0.0", "joblib!=1.0.0"}

    def test_filter_no_matches(self):
        """Test filtering when no packages match."""
        requirements = ["numpy==1.0.0", "pandas==2.0.0"]
        package_names = {"matplotlib", "seaborn"}
        result = filter_packages_by_name(requirements, package_names)
        assert result == []

    def test_filter_empty_requirements(self):
        """Test filtering with empty requirements list."""
        requirements = []
        package_names = {"numpy"}
        result = filter_packages_by_name(requirements, package_names)
        assert result == []

    def test_filter_empty_package_names(self):
        """Test filtering with empty package names set."""
        requirements = ["numpy==1.0.0", "pandas==2.0.0"]
        package_names = set()
        result = filter_packages_by_name(requirements, package_names)
        assert result == []


class TestExcludePackagesByName:
    """Tests for exclude_packages_by_name function."""

    def test_exclude_exact_match(self):
        """Test excluding with exact package name match."""
        requirements = ["numpy==1.0.0", "pandas==2.0.0", "matplotlib==3.0.0"]
        package_names = {"matplotlib"}
        result = exclude_packages_by_name(requirements, package_names)
        assert set(result) == {"numpy==1.0.0", "pandas==2.0.0"}

    def test_exclude_multiple_packages(self):
        """Test excluding multiple packages."""
        requirements = [
            "numpy==1.0.0",
            "pandas==2.0.0",
            "matplotlib==3.0.0",
            "seaborn==0.11.0",
        ]
        package_names = {"matplotlib", "seaborn"}
        result = exclude_packages_by_name(requirements, package_names)
        assert set(result) == {"numpy==1.0.0", "pandas==2.0.0"}

    def test_exclude_no_matches(self):
        """Test excluding when no packages match."""
        requirements = ["numpy==1.0.0", "pandas==2.0.0"]
        package_names = {"matplotlib"}
        result = exclude_packages_by_name(requirements, package_names)
        assert set(result) == {"numpy==1.0.0", "pandas==2.0.0"}

    def test_exclude_empty_requirements(self):
        """Test excluding with empty requirements list."""
        requirements = []
        package_names = {"matplotlib"}
        result = exclude_packages_by_name(requirements, package_names)
        assert result == []

    def test_exclude_empty_package_names(self):
        """Test excluding with empty package names set."""
        requirements = ["numpy==1.0.0", "pandas==2.0.0"]
        package_names = set()
        result = exclude_packages_by_name(requirements, package_names)
        assert set(result) == {"numpy==1.0.0", "pandas==2.0.0"}
