from ..common import CoreObject, PoroGhost
from ...dto.ddragon.item import ItemListDto

from ...utils import version_to_id

class ItemListCore(CoreObject):
    _dto_type = ItemListDto
    _renamed = {}

class Items(PoroGhost):
    _core_types = {ItemListCore}

    def __init__(
            self,
            version
    ):
        kwargs = {"version":version}

        super().__init__(**kwargs)
    
    @property
    def items(self) -> dict:
        return self._data[ItemListCore].items
    
    @property
    def version(self):
        return self._data[ItemListCore].version
    
    @property
    def version_id(self):
        return version_to_id(self.version)