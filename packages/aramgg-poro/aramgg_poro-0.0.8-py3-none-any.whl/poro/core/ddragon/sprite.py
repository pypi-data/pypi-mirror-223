from ..common import CoreObject, PoroGhost
from ...dto.ddragon.sprite import SpriteListDto

from ...utils import version_to_id

class SpriteListCore(CoreObject):
    _dto_type = SpriteListDto
    _renamed = {}

class Sprites(PoroGhost):
    _core_types = {SpriteListCore}

    def __init__(
            self,
            version
    ):
        kwargs = {"version":version}

        super().__init__(**kwargs)
    
    @property
    def sprites(self):
        return self._data[SpriteListCore].sprites
    
    @property
    def champions(self):
        return self.sprites["champion"]
    
    @property
    def passives(self):
        return self.sprites["passive"]
    
    @property
    def spells(self):
        return self.sprites["spell"]
    
    @property
    def version(self):
        return self._data[SpriteListCore].version
    
    @property
    def version_id(self):
        return version_to_id(self.version)
    
    @property
    def items(self):
        return self.sprites["item"]
    
    @property
    def profileicons(self):
        return self.sprites["profileicon"]