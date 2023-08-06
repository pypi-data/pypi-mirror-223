from ...dto.riotapi.summoner import SummonerDto
from ..common import APIObject

class SummonerAPI(APIObject):

    def _get_url(self, region, puuid=None, name=None):
        if puuid!=None:
            url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        elif name!=None:
            url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}"
        
        return url
    
    def get_summoner(self, region, puuid=None, name=None) -> SummonerDto:
        url = self._get_url(region.value.lower(), puuid, name)

        dto = self._client.get(url)[0]

        dto["region"] = region.value

        return SummonerDto(dto)