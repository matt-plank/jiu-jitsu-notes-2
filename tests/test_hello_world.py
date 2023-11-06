def test_get(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.content == b"<h1>Hello, World!</h1>"
