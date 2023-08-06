from ..common import CoreObject, PoroGhost
from ...dto.riotapi.summoner import SummonerDto
from ...data import Region
from typing import Union

class SummonerCore(CoreObject):
    _dto_type = SummonerDto
    _renamed = {
        "profileIconId" : "icon_id",
        "summonerLevel" : "level"
    }

class Summoner(PoroGhost):
    _core_types = {SummonerCore}

    def __init__(
            self,
            region: Union[Region, str],
            puuid: str = None,
            name: str = None,
    ):
        if isinstance(region, str):
            region = Region(region.upper())
        kwargs = {"region":region}

        if puuid is not None:
            kwargs["puuid"] = puuid
        if name is not None:
            kwargs["name"] = name
        super().__init__(**kwargs)
    
    @property
    def accountId(self) -> str:
        return self._data[SummonerCore].accountId
    
    @property
    def puuid(self) -> str:
        return self._data[SummonerCore].puuid
    
    @property
    def id(self) -> str:
        return self._data[SummonerCore].id
    
    @property
    def name(self) -> str:
        return self._data[SummonerCore].name
    
    @property
    def sanitized_name(self) -> str:
        return self.name.replace(" ", "").lower()
    
    @property
    def level(self) -> str:
        return self._data[SummonerCore].level
    
    @property
    def icon_id(self) -> str:
        return self._data[SummonerCore].icon_id
    
    @property
    def region(self) -> Region:
        return Region(self._data[SummonerCore].region)
    
    def match_history(self, start, count) -> "MatchHistory":
        from .match import MatchHistory

        return MatchHistory(self.region.continent, self.puuid, start, count)

    from .match import MatchHistory