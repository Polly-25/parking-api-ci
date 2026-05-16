def test_create_new_client(client):
    new_client_data = {
        "name": "Мария",
        "surname": "Петрова",
        "credit_card": "5555 6666 7777 8888",
        "car_number": "М321ВС77",
    }
    response = client.post("/clients", json=new_client_data)

    assert response.status_code == 201, f"Expected 201," f" got {response.status_code}"

    data = response.get_json()

    assert "id" in data, "Response should contain 'id'"
    assert isinstance(data["id"], int), "'id' should be an integer"

    assert data["name"] == new_client_data["name"]
    assert data["surname"] == new_client_data["surname"]
    assert data["credit_card"] == new_client_data["credit_card"]
    assert data["car_number"] == new_client_data["car_number"]
    client_id = data["id"]
    response_get = client.get(f"/clients/{client_id}")
    assert (
        response_get.status_code == 200
    ), f"Expected 200, got {response_get.status_code}"

    client_data = response_get.get_json()
    assert client_data["name"] == new_client_data["name"]
    assert client_data["surname"] == new_client_data["surname"]
    assert client_data["credit_card"] == new_client_data["credit_card"]
    assert client_data["car_number"] == new_client_data["car_number"]
