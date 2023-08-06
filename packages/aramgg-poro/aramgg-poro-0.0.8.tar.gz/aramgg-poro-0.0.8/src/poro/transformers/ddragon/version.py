from ...core.ddragon.version import VersionListCore
from ...core.ddragon.version import VersionListDto

class VersionTransformer:

    def versionList_dto_to_core(self, value:VersionListDto) -> VersionListCore:
        return VersionListCore(**value)