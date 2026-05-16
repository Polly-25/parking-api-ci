from datetime import datetime

import pytest


@pytest.mark.parking
def test_time_out_after_time_in(client):
    create_client_response = client.post(
        "/clients",
        json={
            "name": "TimeTest",
            "surname": "User",
            "credit_card": "8888777766665555",
            "car_number": "T000TT",
        },
    )
    assert create_client_response.status_code == 201
    client_id = create_client_response.get_json()["id"]

    create_parking_response = client.post(
        "/parkings", json={"address": "Timer", "opened": True, "count_places": 4}
    )
    assert create_parking_response.status_code == 201
    parking_id = create_parking_response.get_json()["id"]

    enter = client.post(
        "/clients_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )
    assert enter.status_code == 201

    enter_data = enter.get_json()
    time_in = enter_data["time_in"]
    assert time_in is not None

    response = client.delete(
        "/clients_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )
    assert response.status_code == 200, f"Failed to exit: {response.data}"

    exit_data = response.get_json()
    time_out = exit_data.get("time_out")
    assert time_out is not None

    time_in_dt = datetime.fromisoformat(time_in)
    time_out_dt = datetime.fromisoformat(time_out)
    assert time_out_dt >= time_in_dt
