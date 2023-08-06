from ..common import APIObject
from ...dto.ddragon.profileicon import ProfileIconListDto

class ProfileIconAPI(APIObject):

    def get_profile_icons(self, version) -> ProfileIconListDto:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/ko_KR/profileicon.json"

        dto = self._client.get(url)[0]
        data = dto["data"]

        return ProfileIconListDto({"version":version, "profile_icons":data})