from ..common import CoreObject, PoroGhost
from ...dto.ddragon.profileicon import ProfileIconListDto

from ...utils import version_to_id

class ProfileIconListCore(CoreObject):
    _dto_type = ProfileIconListDto
    _renamed = {}

class ProfileIcons(PoroGhost):
    _core_types = {ProfileIconListCore}

    def __init__(
            self,
            version
    ):
        kwargs = {"version":version}

        super().__init__(**kwargs)
    
    @property
    def profile_icons(self) -> dict:
        return self._data[ProfileIconListCore].profile_icons
    
    @property
    def version(self):
        return self._data[ProfileIconListCore].version
    
    @property
    def version_id(self):
        return version_to_id(self.version)