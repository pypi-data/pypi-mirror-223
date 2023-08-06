from ...dto.riotapi.match import MatchDto, MatchListDto
from ..common import APIObject

class MatchAPI(APIObject):

    _dto_types = {MatchDto}

    def get_match(self, continent, id) -> MatchDto:
        url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/{id}"

        dto = self._client.get(url)[0]

        # drop metadata
        data = dto["info"]

        data["continent"] = continent.value
        data["id"] = id

        return MatchDto(data)

    def get_matchHistory(self, continent, puuid, start=None, count=None) -> MatchListDto:
        if start is not None:
            url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={self._queue}&start={start}&count={count}"
            data = self._client.get(url)[0]
            dto = {
                "match_ids" : data,
                "continent" : continent.value,
                "puuid" : puuid,
                "queue" : self._queue,
                "start" : start,
                "count" : count
            }

            return MatchListDto(dto)
        else:
            start = 0
            count = 100

            dto = {
                "match_ids" : [],
                "continent" : continent.value,
                "puuid" : puuid,
                "queue" : self._queue,
                "start" : start
            }

            while True:
                url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={self._queue}&start={start}&count={count}"
                data = self._client.get(url)[0]
                dto["match_ids"].extend(data)

                start += 100

                if len(dto["match_ids"])%100!=0:
                    break
            
            dto["count"] = len(dto["match_ids"])
            
            return MatchListDto(dto)