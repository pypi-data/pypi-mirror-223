from ..common import CoreObject, PoroGhost
from ...dto.ddragon.version import VersionListDto

class VersionListCore(CoreObject):
    _dto_type = VersionListDto
    _renamed = {}

class Versions(PoroGhost):
    _core_types = {VersionListCore}

    def __init__(self):

        super().__init__()
    
    @property
    def versions(self):
        return self._data[VersionListCore].versions