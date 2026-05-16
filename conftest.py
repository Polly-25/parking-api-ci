import pytest

from .models import Client, ClientParking, Parking, db
from .myapp import create_app


@pytest.fixture
def app():
    app = create_app(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "TESTING": True,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database(app):
    with app.app_context():
        client1 = Client(
            name="Иван",
            surname="Иванов",
            credit_card="1234567890123456",
            car_number="А123ВС77",
        )
        client2 = Client(
            name="Петр",
            surname="Петров",
            credit_card="1111222233334444",
            car_number="В456МН77",
        )

        parking1 = Parking(
            address="ул. Ленина, д.1",
            opened=True,
            count_places=10,
            count_available_places=8,
        )

        db.session.add_all([client1, client2, parking1])
        db.session.commit()
        parking_log = ClientParking(
            client_id=client1.id,
            parking_id=parking1.id,
            time_in=datetime.datetime(2026, 5, 13, 10, 0, 0),
            time_out=datetime.datetime(2026, 5, 13, 12, 0, 0),
        )

        db.session.add(parking_log)
        db.session.commit()

        yield {
            "clients": [client1, client2],
            "parking": parking1,
            "parking_log": parking_log,
        }

        db.session.remove()
