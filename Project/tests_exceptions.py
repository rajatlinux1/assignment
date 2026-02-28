import pytest
from rest_framework.exceptions import ValidationError

from Project.exceptions import custom_exception_handler


@pytest.mark.django_db
class TestCustomExceptionHandler:

    def test_validation_error_handler(self):
        """Test that DRF validation errors are cleanly formatted"""
        # Simulate a DRF validation error
        exc = ValidationError({"field": ["This field is required."]})
        context = {"view": "MockView"}

        response = custom_exception_handler(exc, context)

        assert response is not None
        assert response.status_code == 400
        assert response.data["error"] is True
        assert response.data["message"] == "Validation or input error."
        assert "field" in response.data["details"]

    def test_unhandled_exception_handler(self):
        """Test that unhandled 500 exceptions are gracefully intercepted and formatted as JSON"""
        # Simulate an unexpected system crash
        exc = ValueError("A critical database failure occurred")
        context = {"view": "MockView"}

        response = custom_exception_handler(exc, context)

        assert response is not None
        assert response.status_code == 500
        assert response.data["error"] is True
        assert response.data["message"] == "An unexpected server error occurred."
        assert response.data["details"] == "A critical database failure occurred"
