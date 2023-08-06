from ..common import APIObject
from ...dto.ddragon.perk import PerkListDto, PerkIconListDto
from ...utils import img_to_str

class PerkAPI(APIObject):

    def get_perks(self, version) -> PerkListDto:
        perks_url = f"https://raw.communitydragon.org/{version[:5]}/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"
        perks = self._client.get(perks_url)[0]
        for perk in perks:
            if perk["id"]==7000:
                perks.remove(perk)
                break
        
        perk_styles_url = f"https://raw.communitydragon.org/{version[:5]}/plugins/rcp-be-lol-game-data/global/default/v1/perkstyles.json"
        styles = self._client.get(perk_styles_url)[0]["styles"]

        return PerkListDto({"version":version, "perks":perks, "styles":styles})

    def get_perk_icons(self, version) -> PerkIconListDto:
        _perks = self.get_perks(version)
        perks = _perks["perks"]
        styles = _perks["styles"]
        icons = {}

        for perk in perks:
            path = perk["iconPath"][perk["iconPath"].find("v1"):]
            url = f"https://raw.communitydragon.org/{version[:5]}/plugins/rcp-be-lol-game-data/global/default/{path}".lower()

            icons[perk["id"]] = img_to_str(self._client.get(url)[0])
        
        for style in styles:
            path = style["iconPath"][style["iconPath"].find("v1"):]
            url = f"https://raw.communitydragon.org/{version[:5]}/plugins/rcp-be-lol-game-data/global/default/{path}".lower()

            icons[perk["id"]] = img_to_str(self._client.get(url)[0])

        return PerkIconListDto({"version":version, "icons":icons})