from ..common import CoreObject, PoroGhost
from ...dto.ddragon.spell import SpellListDto

from ...utils import version_to_id

class SpellListCore(CoreObject):
    _dto_type = SpellListDto
    _renamed = {}

class Spells(PoroGhost):
    _core_types = {SpellListCore}

    def __init__(
            self,
            version
    ):
        kwargs = {"version":version}

        super().__init__(**kwargs)
    
    @property
    def spells(self) -> dict:
        return self._data[SpellListCore].spells
    
    @property
    def version(self):
        return self._data[SpellListCore].version
    
    @property
    def version_id(self):
        return version_to_id(self.version)