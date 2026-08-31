"""Tests for utility functions."""

from datetime import UTC, datetime

from src.core.utils import camel_to_snake, utcnow


class TestCamelToSnake:
    """Tests for camel_to_snake function."""

    def test_simple_camel_case(self) -> None:
        """Test conversion of simple camel case string."""
        assert camel_to_snake("UserProfile") == "user_profiles"

    def test_single_word(self) -> None:
        """Test conversion of single word."""
        assert camel_to_snake("User") == "users"

    def test_empty_string(self) -> None:
        """Test conversion of empty string."""
        assert camel_to_snake("") == ""

    def test_already_snake(self) -> None:
        """Test conversion of already snake case string."""
        assert camel_to_snake("user_profile") == "user_profiles"

    def test_single_lowercase(self) -> None:
        """Test conversion of single lowercase word."""
        assert camel_to_snake("user") == "users"

    def test_orm_removal(self) -> None:
        """Test that ORM suffix is removed."""
        assert camel_to_snake("UserORM") == "users"


class TestUtcNow:
    """Tests for utcnow function."""

    def test_returns_datetime(self) -> None:
        """Test that utcnow returns a datetime object."""
        result: datetime = utcnow()
        assert isinstance(result, datetime)

    def test_returns_utc_timezone(self) -> None:
        """Test that utcnow returns UTC timezone."""
        result: datetime = utcnow()
        assert result.tzinfo == UTC

    def test_current_time(self) -> None:
        """Test that utcnow returns current time."""
        before = datetime.now(UTC)
        result = utcnow()
        after = datetime.now(UTC)
        assert before <= result <= after
