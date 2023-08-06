from .riotapi import (
    SummonerTransformer,
    MatchTransformer
)

from .ddragon import (
    VersionTransformer,
    ChampionTransformer,
    ItemTransformer,
    PerkTransformer,
    SpellTransformer,
    ProfileIconTransformer,
    SpriteTransformer
)

_transformers = {
    SummonerTransformer(),
    MatchTransformer(),
    VersionTransformer(),
    ChampionTransformer(),
    ItemTransformer(),
    PerkTransformer(),
    SpellTransformer(),
    ProfileIconTransformer(),
    SpriteTransformer()
}