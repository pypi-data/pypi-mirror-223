from ..common import APIObject
from ...dto.ddragon.version import VersionListDto

class VersionAPI(APIObject):

    def get_versions(self) -> VersionListDto:
        url = "https://ddragon.leagueoflegends.com/api/versions.json"

        dto = self._client.get(url)[0]
        
        return VersionListDto({"versions":dto})