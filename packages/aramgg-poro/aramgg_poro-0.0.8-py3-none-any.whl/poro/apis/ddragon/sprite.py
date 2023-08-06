from ...dto.ddragon.sprite import SpriteListDto
from ..common import APIObject
from ...utils import img_to_str, get_int_from_str

class SpriteAPI(APIObject):
    def get_sprites(self, version) -> SpriteListDto:
        _sprite = {}

        _champion_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/ko_KR/championFull.json"
        _champions = self._client.get(_champion_url)[0]["data"]
        last_champion = _champions[list(_champions.keys())[-1]]
        _sprite["champion"] = get_int_from_str(last_champion["image"]["sprite"])
        _sprite["spell"] = get_int_from_str(last_champion["spells"][-1]["image"]["sprite"])
        _sprite["passive"] = get_int_from_str(last_champion["passive"]["image"]["sprite"])

        _item_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/ko_KR/item.json"
        _item = self._client.get(_item_url)[0]["data"]
        last_item = _item[list(_item.keys())[-1]]
        _sprite["item"] = get_int_from_str(last_item["image"]["sprite"])

        _profileicon_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/ko_KR/profileicon.json"
        _profileicon = self._client.get(_profileicon_url)[0]["data"]
        last_pi = _profileicon[list(_profileicon.keys())[-1]]
        _sprite["profileicon"] = get_int_from_str(last_pi["image"]["sprite"])

        sprite = {}

        for k, v in _sprite.items():
            sprite[k] = {}
            for i in range(v+1):
                value = k+str(i)
                sprite[k][value] = self._get_sprite_str(version, value)
    
        return SpriteListDto({"version":version, "sprites":sprite})
    
    def _get_sprite_str(self, version, value):
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/sprite/{value}.png"

        img = self._client.get(url)[0]
        str = img_to_str(img)
        
        return str