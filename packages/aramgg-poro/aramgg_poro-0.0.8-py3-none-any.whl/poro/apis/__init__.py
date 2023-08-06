from .riotapi import (
    SummonerAPI,
    MatchAPI
)
from .ddragon import (
    VersionAPI,
    ChampionAPI,
    ItemAPI,
    PerkAPI,
    SpellAPI,
    ProfileIconAPI,
    SpriteAPI
)
from .common import RequestClient

_client = RequestClient()

_apis = {
    SummonerAPI(_client),
    MatchAPI(_client),
    VersionAPI(_client),
    ChampionAPI(_client),
    ItemAPI(_client),
    PerkAPI(_client),
    SpellAPI(_client),
    ProfileIconAPI(_client),
    SpriteAPI(_client)
}