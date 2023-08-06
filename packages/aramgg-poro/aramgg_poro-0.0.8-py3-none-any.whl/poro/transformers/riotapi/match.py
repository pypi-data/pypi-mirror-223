from ...core.riotapi.match import MatchListCore, MatchCore
from ...dto.riotapi.match import MatchListDto, MatchDto

class MatchTransformer:

    def matchList_dto_to_core(self, value:MatchListDto) -> MatchListCore:
        return MatchListCore(**value)
    
    def match_dto_to_core(self, value:MatchDto) -> MatchCore:
        return MatchCore(**value)