def test_create_new_parking(client):
    new_parking_data = {
        "address": "Примерная улица, 10",
        "opened": True,
        "count_places": 20,
        "count_available_places": 20,
    }
    response = client.post("/parkings", json=new_parking_data)
    assert response.status_code == 201

    data = response.get_json()
    assert data["address"] == new_parking_data["address"]
    assert data["opened"] == new_parking_data["opened"]
    assert data["count_places"] == new_parking_data["count_places"]
    expected_count = new_parking_data["count_available_places"]
    actual_count = data["count_available_places"]

    assert actual_count == expected_count
    assert "id" in data
