from ...dto.ddragon.champion import ChampionListDto
from ...core.ddragon.champion import ChampionListCore

class ChampionTransformer:
    
    def champion_list_dto_to_core(self, value:ChampionListDto) -> ChampionListCore:
        return ChampionListCore(**value)