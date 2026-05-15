import pytest
@pytest.mark.parking
def test_parking_exit(client):

    client_data = {
        "name": "Выездов",
        "surname": "Тестовый",
        "credit_card": "9999888877776666",
        "car_number": "B321CD"
    }
    client_resp = client.post("/clients", json=client_data)
    assert client_resp.status_code == 201
    client_id = client_resp.get_json()["id"]
    parking_data = {
        "address": "Улица Парковая, 2",
        "opened": True,
        "count_places": 15,
        "count_available_places": 15
    }
    parking_resp = client.post("/parkings", json=parking_data)
    assert parking_resp.status_code == 201
    parking_id = parking_resp.get_json()["id"]

    enter_data = {
        "client_id": client_id,
        "parking_id": parking_id
    }
    enter_resp = client.post("/clients_parkings", json=enter_data)
    assert enter_resp.status_code == 201

    exit_data = {
        "client_id": client_id,
        "parking_id": parking_id
    }
    exit_resp = client.delete("/clients_parkings", json=exit_data)
    assert exit_resp.status_code == 200

    exit_json = exit_resp.get_json()
    assert exit_json["client_id"] == client_id
    assert exit_json["parking_id"] == parking_id
    assert "time_out" in exit_json
