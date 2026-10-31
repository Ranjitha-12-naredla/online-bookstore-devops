import app as bookstore

def test_health_endpoint():
    client = bookstore.app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_home_page():
    client = bookstore.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Online Bookstore" in response.data
