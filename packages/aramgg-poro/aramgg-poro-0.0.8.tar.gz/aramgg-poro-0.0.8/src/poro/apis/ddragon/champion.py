from ..common import APIObject
from ...dto.ddragon.champion import ChampionListDto

class ChampionAPI(APIObject):

    def get_champions(self, version) -> ChampionListDto:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/ko_KR/championFull.json"

        dto = self._client.get(url)[0]
        data = dto["data"]

        return ChampionListDto({"version":version, "champions":data})