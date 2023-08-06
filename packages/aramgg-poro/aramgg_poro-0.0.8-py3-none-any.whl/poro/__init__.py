from ._configuration import PoroConfiguration as _PoroConfiguration

configuration = _PoroConfiguration()

def set_riot_api_key(key):
    configuration._pipeline.set_riot_api_key(key)

from .core import (
    Summoner,
    MatchHistory,
    Match,
    Versions,
    Champions,
    Items,
    Perks,
    Spells,
    Sprites,
    ProfileIcons,
    PerkIcons
)

from .data import (
    Region,
    Continent
)

from .poro import (
    get_versions
)

from .utils import (
    img_to_str
)