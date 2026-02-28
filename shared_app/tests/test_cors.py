import pytest
from corsheaders.middleware import CorsMiddleware
from django.http import HttpResponse
from django.test import RequestFactory


@pytest.fixture
def cors_middleware():
    def get_response(request):
        return HttpResponse("OK")

    return CorsMiddleware(get_response)


def test_cors_allowed_origin(cors_middleware):
    rf = RequestFactory()
    request = rf.get("/", HTTP_ORIGIN="http://localhost:5173")

    response = cors_middleware(request)

    assert "Access-Control-Allow-Origin" in response
    assert response["Access-Control-Allow-Origin"] == "http://localhost:5173"


def test_cors_disallowed_origin(cors_middleware):
    rf = RequestFactory()
    request = rf.get("/", HTTP_ORIGIN="http://malicious.com")

    response = cors_middleware(request)

    assert "Access-Control-Allow-Origin" not in response
