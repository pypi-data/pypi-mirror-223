from ...dto.ddragon.profileicon import ProfileIconListDto
from ...core.ddragon.profileicon import ProfileIconListCore

class ProfileIconTransformer:
    
    def profile_icon_list_dto_to_core(self, value:ProfileIconListDto) -> ProfileIconListCore:
        return ProfileIconListCore(**value)