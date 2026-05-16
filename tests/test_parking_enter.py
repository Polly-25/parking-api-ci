import pytest


@pytest.mark.parking
def test_parking_enter(client):
    client_data = {
        "name": "Иван",
        "surname": "Тестов",
        "credit_card": "1234567812345678",
        "car_number": "A123BC",
    }
    client_resp = client.post("/clients", json=client_data)
    assert client_resp.status_code == 201
    client_id = client_resp.get_json()["id"]

    parking_data = {
        "address": "Большая улица, 1",
        "opened": True,
        "count_places": 10,
        "count_available_places": 10,
    }
    parking_resp = client.post("/parkings", json=parking_data)
    assert parking_resp.status_code == 201
    parking_id = parking_resp.get_json()["id"]

    enter_data = {"client_id": client_id, "parking_id": parking_id}
    enter_resp = client.post("/clients_parkings", json=enter_data)
    assert enter_resp.status_code == 201

    enter_json = enter_resp.get_json()
    assert enter_json["client_id"] == client_id
    assert enter_json["parking_id"] == parking_id
    assert "time_in" in enter_json
