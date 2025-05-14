import pytest
from flask import Flask
from api_gateway.routes.health_check import health_bp  # Adjust import

@pytest.fixture
def client(app):
    app.register_blueprint(health_bp, url_prefix="/health")
    return app.test_client()

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}