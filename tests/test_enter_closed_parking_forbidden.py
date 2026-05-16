import pytest


@pytest.mark.parking
def test_enter_closed_parking_forbidden(client):
    client_resp = client.post(
        "/clients",
        json={
            "name": "Test",
            "surname": "Closed",
            "credit_card": "1111222233334444",
            "car_number": "C000XX",
        },
    )
    client_id = client_resp.get_json()["id"]

    parking_resp = client.post(
        "/parkings",
        json={
            "address": "NoOpen",
            "opened": False,
            "count_places": 20,
            "count_available_places": 20,
        },
    )
    parking_id = parking_resp.get_json()["id"]

    res = client.post(
        "/clients_parkings",
        json={
            "client_id": client_id,
            "parking_id": parking_id
        }
    )
    assert res.status_code == 400
