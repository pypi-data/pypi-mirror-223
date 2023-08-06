from ...dto.ddragon.sprite import SpriteListDto
from ...core.ddragon.sprite import SpriteListCore

class SpriteTransformer:
    
    def sprite_list_dto_to_core(self, value:SpriteListDto) -> SpriteListCore:
        return SpriteListCore(**value)