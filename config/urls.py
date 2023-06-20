import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


def filter_by_keys(source: dict, keys: list[str]) -> dict:
    filtered_data = {}

    for key, value in source.items():
        if key in keys:
            filtered_data[key] = value

    return filtered_data


@dataclass
class Pokemon:
    id: int
    name: str
    height: int
    weight: int
    base_experience: int

    @classmethod
    def from_raw_data(cls, raw_data: dict) -> "Pokemon":
        filtered_data = filter_by_keys(
            raw_data,
            cls.__dataclass_fields__.keys(),
        )
        return cls(**filtered_data)


# ============================================
# Simulate the CACHE
# ============================================
TTL = timedelta(seconds=5)
POKEMONS: dict[str, list[Pokemon, datetime]] = {}


def get_pokemon_from_api(name: str) -> Pokemon:
    url = settings.POKEAPI_BASE_URL + f"/{name}"
    response = requests.get(url)
    raw_data = response.json()

    return Pokemon.from_raw_data(raw_data)


def _get_pokemon(name) -> Pokemon:
    """
    Take pokemon from the cache or
    fetch it from the API and then save it to the cache.
    """

    if name in POKEMONS:
        pokemon, created_at = POKEMONS[name]

        if datetime.now() > created_at + TTL:
            del POKEMONS[name]
            return _get_pokemon(name)
    else:
        pokemon: Pokemon = get_pokemon_from_api(name)
        POKEMONS[name] = [pokemon, datetime.now()]

    return pokemon


def _get_pokemon_from_cache(name: str):
    pokemon: Pokemon = _get_pokemon(name)
    return HttpResponse(
        content_type="application/json", content=json.dumps(asdict(pokemon)), status=200
    )


def _delete_pokemon_from_cache(name: str):
    if name in POKEMONS:
        del POKEMONS[name]
        response_data = json.dumps({"message": "Pokemon removed from cache"})
        return HttpResponse(
            content=response_data, content_type="application/json", status=204
        )
    else:
        response_data = json.dumps({"message": "Pokemon not found in cache"})
        return HttpResponse(
            content=response_data, content_type="application/json", status=404
        )


@csrf_exempt
def pokemon_handler(request, name: str):
    if request.method == "GET":
        return _get_pokemon_from_cache(name)
    if request.method == "DELETE":
        return _delete_pokemon_from_cache(name)
    else:
        response_data = json.dumps({"message": "Not allowed"})
        return HttpResponse(
            content=response_data, content_type="application/json", status=405
        )


def get_pokemon_for_mobile(request, name: str):
    pokemon: Pokemon = _get_pokemon(name)
    result = filter_by_keys(
        asdict(pokemon),
        ["id", "name", "base_experience"],
    )

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )


def get_pokemons_list(request):
    pokemons_list = []
    for pokemon, timestamp in POKEMONS.values():
        pokemons_list.append(asdict(pokemon))

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(pokemons_list),
    )


urlpatterns = [
    path("api/pokemon/", get_pokemons_list),
    path("api/pokemon/<str:name>/", pokemon_handler),
    path("api/pokemon/mobile/<str:name>/", get_pokemon_for_mobile),
]
