from ..common import CoreObject, PoroGhost
from ...dto.ddragon.perk import PerkListDto, PerkIconListDto

from ...utils import version_to_id

class PerkListCore(CoreObject):
    _dto_type = PerkListDto
    _renamed = {}

class PerkIconListCore(CoreObject):
    _dto_type = PerkIconListDto
    _renamed = {}

class Perks(PoroGhost):
    _core_types = {PerkListCore}

    def __init__(
            self,
            version
    ):
        kwargs = {"version":version}

        super().__init__(**kwargs)
    
    @property
    def perks(self) -> list:
        return self._data[PerkListCore].perks
    
    @property
    def styles(self):
        return self._data[PerkListCore].styles
    
    @property
    def version(self):
        return self._data[PerkListCore].version
    
    @property
    def version_id(self):
        return version_to_id(self.version)

class PerkIcons(PoroGhost):
    _core_types = {PerkIconListCore}

    def __init__(
            self,
            version
    ):
        kwargs = {"version":version}

        super().__init__(**kwargs)
    
    @property
    def icons(self):
        return self._data[PerkIconListCore].icons
    
    @property
    def version(self):
        return self._data[PerkIconListCore].version
    
    @property
    def version_id(self):
        return version_to_id(self.version)