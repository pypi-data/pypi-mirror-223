from ..common import APIObject
from ...dto.ddragon.item import ItemListDto

class ItemAPI(APIObject):

    def get_items(self, version) -> ItemListDto:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/ko_KR/item.json"

        dto = self._client.get(url)[0]
        data = dto["data"]

        return ItemListDto({"version":version, "items":data})