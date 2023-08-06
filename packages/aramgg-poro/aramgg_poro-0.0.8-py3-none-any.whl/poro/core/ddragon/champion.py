from ..common import CoreObject, PoroGhost
from ...dto.ddragon.champion import ChampionListDto

from ...utils import version_to_id

class ChampionListCore(CoreObject):
    _dto_type = ChampionListDto
    _renamed = {}

class Champions(PoroGhost):
    _core_types = {ChampionListCore}

    def __init__(
            self,
            version
    ):
        kwargs = {"version":version}

        super().__init__(**kwargs)
    
    @property
    def champions(self) -> dict:
        return self._data[ChampionListCore].champions
    
    @property
    def version(self):
        return self._data[ChampionListCore].version
    
    @property
    def version_id(self):
        return version_to_id(self.version)