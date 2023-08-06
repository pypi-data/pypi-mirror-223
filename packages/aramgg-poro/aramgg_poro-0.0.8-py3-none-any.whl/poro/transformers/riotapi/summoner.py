from ...core.riotapi.summoner import SummonerCore
from ...dto.riotapi.summoner import SummonerDto

class SummonerTransformer:

    def summoner_dto_to_core(self, value:SummonerDto) -> SummonerCore:
        return SummonerCore(**value)
    
    def test(self, value:list) -> SummonerCore:
        return SummonerCore(**value)