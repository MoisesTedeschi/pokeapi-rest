import requests


poke_endpoint = "https://pokeapi.co/api/v2"


def test_status_code_200():
    response = requests.get(poke_endpoint)
    assert response.status_code == 200


def test_type_pokemon_status_code_200():
    response = requests.get(f'{poke_endpoint}/type/grass')
    assert response.status_code == 200


def test_get_content_type_equals_json():
    response = requests.get(poke_endpoint)
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
