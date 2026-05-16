import datetime

from flask import Flask, jsonify, request


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    from .models import Client, ClientParking, Parking, db

    db.init_app(app)

    @app.route("/clients", methods=["GET"])
    def get_clients():
        data_clients = Client.query.all()
        list_of_clients = []
        for client in data_clients:
            list_of_clients.append(
                {
                    "id": client.id,
                    "name": client.name,
                    "surname": client.surname,
                    "credit_card": client.credit_card,
                }
            )
        return jsonify(list_of_clients), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client_for_id(client_id):
        client = db.session.get(Client, client_id)
        if client is None:
            return jsonify({"error": "Client not found"}), 404
        return (
            jsonify(
                {
                    "id": client.id,
                    "name": client.name,
                    "surname": client.surname,
                    "credit_card": client.credit_card,
                    "car_number": client.car_number,
                }
            ),
            200,
        )

    @app.route("/clients", methods=["POST"])
    def add_new_client():
        try:
            data = request.json
            name = data.get("name")
            surname = data.get("surname")
            if not name or not surname:
                return jsonify({"error": "Name and surname are required"}), 400
            credit_card = data.get("credit_card")
            car_number = data.get("car_number")
            new_client = Client(
                name=name,
                surname=surname,
                credit_card=credit_card,
                car_number=car_number,
            )
            db.session.add(new_client)
            db.session.commit()
            id = new_client.id
            return (
                jsonify(
                    {
                        "id": id,
                        "name": new_client.name,
                        "surname": new_client.surname,
                        "credit_card": new_client.credit_card,
                        "car_number": new_client.car_number,
                    }
                ),
                201,
            )
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route("/parkings", methods=["POST"])
    def add_new_parking_zone():
        try:
            data = request.json
            address = data.get("address")
            opened = data.get("opened")
            count_places = data.get("count_places")
            count_available_places = count_places if opened else 0
            if not address or count_places is None:
                return (
                    jsonify({"error": "Address and count_places are required"}),
                    400,
                )
            parking_zone = Parking(
                address=address,
                opened=opened,
                count_places=count_places,
                count_available_places=count_available_places,
            )
            db.session.add(parking_zone)
            db.session.commit()
            parking_id = parking_zone.id
            available_places = parking_zone.count_available_places
            response = jsonify(
                {
                    "id": parking_id,
                    "address": parking_zone.address,
                    "opened": parking_zone.opened,
                    "count_places": parking_zone.count_places,
                    "count_available_places": available_places,
                }
            )

            return response, 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route("/clients_parkings", methods=["POST"])
    def parking_enter():
        data = request.json
        client_id = data.get("client_id")
        parking_id = data.get("parking_id")
        parking = db.session.get(Parking, parking_id)
        if parking is None:
            return jsonify({"error": "Parking not found"}), 404
        if not parking.opened:
            return jsonify({"error": "Parking is closed"}), 400
        if parking.count_available_places <= 0:
            return jsonify({"error": "No available places"}), 400

        new_parking_record = ClientParking(
            client_id=client_id, parking_id=parking_id, time_in=datetime.datetime.now()
        )

        db.session.add(new_parking_record)
        parking.count_available_places -= 1
        db.session.commit()
        return (
            jsonify(
                {
                    "id": new_parking_record.id,
                    "client_id": new_parking_record.client_id,
                    "parking_id": new_parking_record.parking_id,
                    "time_in": new_parking_record.time_in.isoformat(),
                }
            ),
            201,
        )

    @app.route("/clients_parkings", methods=["DELETE"])
    def leave_the_parking_lot():
        data = request.json
        client_id = data.get("client_id")
        parking_id = data.get("parking_id")
        parking = db.session.get(Parking, parking_id)
        client = db.session.get(Client, client_id)
        if parking is None:
            return jsonify({"error": "Parking not found"}), 404
        if not client.credit_card:
            return jsonify({"error": "Client hasnt a credit card"}), 400
        parking_record = (
            db.session.query(ClientParking)
            .filter_by(client_id=client_id, parking_id=parking_id)
            .first()
        )
        if parking_record is None:
            return jsonify({"error": "No parking record found"}), 404
        parking.count_available_places += 1
        parking_record.time_out = datetime.datetime.now()
        db.session.commit()
        return (
            jsonify(
                {
                    "id": parking_record.id,
                    "client_id": parking_record.client_id,
                    "parking_id": parking_record.parking_id,
                    "time_in": parking_record.time_in.isoformat(),
                    "time_out": parking_record.time_out.isoformat(),
                }
            ),
            200,
        )

    return app
