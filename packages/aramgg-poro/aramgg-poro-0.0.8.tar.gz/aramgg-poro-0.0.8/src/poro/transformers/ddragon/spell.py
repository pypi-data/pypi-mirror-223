from ...dto.ddragon.spell import SpellListDto
from ...core.ddragon.spell import SpellListCore

class SpellTransformer:
    
    def spell_list_dto_to_core(self, value:SpellListDto) -> SpellListCore:
        return SpellListCore(**value)