from ..common import APIObject
from ...dto.ddragon.spell import SpellListDto

class SpellAPI(APIObject):

    def get_spells(self, version) -> SpellListDto:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/ko_KR/summoner.json"

        dto = self._client.get(url)[0]
        data = dto["data"]

        return SpellListDto({"version":version, "spells":data})