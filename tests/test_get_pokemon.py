import pytest
import requests

HOST = "http://localhost:8000"


@pytest.mark.parametrize(
    "name, expected_json",
    [
        (
            "ditto",
            {
                "id": 132,
                "name": "ditto",
                "height": 3,
                "weight": 40,
                "base_experience": 101,
            },
        ),
        (
            "pikachu",
            {
                "id": 25,
                "name": "pikachu",
                "height": 4,
                "weight": 60,
                "base_experience": 112,
            },
        ),
    ],
)
def test_get_pokemon(name, expected_json):
    url = f"{HOST}/api/pokemon/{name}"
    response = requests.get(url)
    assert response.json() == expected_json


@pytest.mark.parametrize(
    "name, expected_json",
    [
        (
            "pikachu",
            {"id": 25, "name": "pikachu", "base_experience": 112},
        ),
    ],
)
def test_get_pokemon_mobile(name, expected_json):
    url = f"{HOST}/api/pokemon/mobile/{name}"
    response = requests.get(url)
    assert response.json() == expected_json


def test_get_pokemons_list():
    url = f"{HOST}/api/pokemon/"
    response = requests.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "name, expected_status_code",
    [
        ("pikachu", 204),
        ("nonexistentpokemon", 404),
    ],
)
def test_delete_pokemon(name, expected_status_code):
    if expected_status_code == 204:
        requests.get(f"{HOST}/api/pokemon/{name}")

    response = requests.delete(f"{HOST}/api/pokemon/{name}")
    assert response.status_code == expected_status_code
