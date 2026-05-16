from ..models import db
from ..factories import ClientFactory, ParkingFactory


def test_create_client(client, init_database):
    client_obj = ClientFactory()
    db.session.commit()
    response = client.post(
        "/clients",
        json={
            "name": client_obj.name,
            "surname": client_obj.surname,
            "credit_card": client_obj.credit_card,
            "car_number": client_obj.car_number,
        },
    )
    assert response.status_code == 201, \
        f"Expected 201," \
        f" got {response.status_code}"
    assert response.get_json()["name"] == client_obj.name


def test_create_parking(client, init_database):
    parking_obj = ParkingFactory.build()
    response = client.post(
        "/parkings",
        json={
            "address": parking_obj.address,
            "opened": parking_obj.opened,
            "count_places": parking_obj.count_places,
        },
    )
    assert response.status_code == 201, \
        f"Expected 201," \
        f" got {response.status_code}"
    assert response.get_json()["address"] == parking_obj.address
