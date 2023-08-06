from ...dto.ddragon.perk import PerkListDto, PerkIconListDto
from ...core.ddragon.perk import PerkListCore, PerkIconListCore

class PerkTransformer:
    
    def perk_list_dto_to_core(self, value:PerkListDto) -> PerkListCore:
        return PerkListCore(**value)
    
    def perk_icon_list_dto_to_core(self, value:PerkIconListDto) -> PerkIconListCore:
        return PerkIconListCore(**value)