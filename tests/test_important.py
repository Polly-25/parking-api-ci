import pytest


@pytest.mark.parametrize(
    "endpoint, method",
    [
        ("/clients", "get"),
    ],
)
def test_get_all_resources(client, endpoint, method):
    if method == "get":
        response = client.get(endpoint)
        assert response.status_code == 200, f"Failed on {endpoint}"
        assert response.json is not None


def test_get_client_by_id(client, init_database):
    client_id = init_database["clients"][0].id

    response = client.get(f"/clients/{client_id}")
    assert response.status_code == 200, f"Client with id {client_id} not found"
    assert response.json["id"] == client_id
