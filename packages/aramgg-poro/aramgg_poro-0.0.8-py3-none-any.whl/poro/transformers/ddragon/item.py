from ...dto.ddragon.item import ItemListDto
from ...core.ddragon.item import ItemListCore

class ItemTransformer:
    
    def item_list_dto_to_core(self, value:ItemListDto) -> ItemListCore:
        return ItemListCore(**value)