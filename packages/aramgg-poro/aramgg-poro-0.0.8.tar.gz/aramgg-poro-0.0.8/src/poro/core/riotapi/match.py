from ..common import CoreObject, PoroGhost
from ...dto.riotapi.match import MatchDto, MatchListDto
from ...data import Region, Continent
from typing import Union

from ...utils import version_to_id, match_version_to_version

class MatchListCore(CoreObject):
    _dto_type = MatchListDto
    _renamed = {}

class ParticipantCore(CoreObject):
    _renamed = {
        "summoner1Id": "summonerSpell1Id",
        "summoner2Id": "summonerSpell2Id"
    }

    def __call__(self, **kwargs):
        perks = kwargs.pop("perks", {})
        stat_perks = perks.pop("statPerks", {})

        styles = perks.pop("styles", [])
        selections = []
        [[selections.append(s) for s in style["selections"]] for style in styles]
        self.main_perk1_key = selections[0]["perk"]
        self.main_perk1_vars = [selections[0].pop("var1"), selections[0].pop("var2"), selections[0].pop("var3")]
        self.main_perk2_key = selections[1]["perk"]
        self.main_perk2_vars = [selections[1].pop("var1"), selections[1].pop("var2"), selections[1].pop("var3")]
        self.main_perk3_key = selections[2]["perk"]
        self.main_perk3_vars = [selections[2].pop("var1"), selections[2].pop("var2"), selections[2].pop("var3")]
        self.main_perk4_key = selections[3]["perk"]
        self.main_perk4_vars = [selections[3].pop("var1"), selections[3].pop("var2"), selections[3].pop("var3")]
        self.sub_perk1_key = selections[4]["perk"]
        self.sub_perk1_vars = [selections[4].pop("var1"), selections[4].pop("var2"), selections[4].pop("var3")]
        self.sub_perk2_key = selections[5]["perk"]
        self.sub_perk2_vars = [selections[5].pop("var1"), selections[5].pop("var2"), selections[5].pop("var3")]
        self.shard1_key = stat_perks["defense"]
        self.shard2_key = stat_perks["flex"]
        self.shard3_key = stat_perks["offense"]
        self.champion_key = kwargs.get("championId", None)
        self.champion_name = kwargs.get("championName", None)
        self.participant_id = kwargs.get("participantId", None)
        self.puuid = kwargs.get("puuid", None)
        self.summoner_name = kwargs.get("summonerName", None)
        self.summoner_level = kwargs.get("summonerLevel", None)
        self.profileicon_key = kwargs.get("profileIcon", None)
        self.summoner_spell1_key = kwargs.get("summoner1Id", None)
        self.summoner_spell2_key = kwargs.get("summoner2Id", None)
        self.team_key = str(kwargs.get("teamId", None))
        self.assists = kwargs.pop("assists", None)
        self.bounty_level = kwargs.pop("bountyLevel", None)
        self.champion_experience = kwargs.pop("champExperience", None)
        self.champion_level = kwargs.pop("champLevel", None)
        self.champion_transform = kwargs.pop("championTransform", None)
        self.challenges = kwargs.pop("challenges", dict)
        self.damage_self_mitigated = kwargs.pop("damageSelfMitigated", None)
        self.deaths = kwargs.pop("deaths", None)
        self.double_kills = kwargs.pop("doubleKills", None)
        self.first_blood = kwargs.pop("firstBloodKill", None)
        self.first_turret_kill = kwargs.pop("firstTowerKill", None)
        self.gold_earned = kwargs.pop("goldEarned", None)
        self.gold_spent = kwargs.pop("goldSpent", None)
        self.inhibitor_kills = kwargs.pop("inhibitorKills", None)
        self.inhibitors_lost = kwargs.pop("inhibitorsLost", None)
        self.item0_key = kwargs.pop("item0", None)
        self.item1_key = kwargs.pop("item1", None)
        self.item2_key = kwargs.pop("item2", None)
        self.item3_key = kwargs.pop("item3", None)
        self.item4_key = kwargs.pop("item4", None)
        self.item5_key = kwargs.pop("item5", None)
        self.item6_key = kwargs.pop("item6", None)
        self.items_purchased = kwargs.pop("itemsPurchased", None)
        self.killing_sprees = kwargs.pop("killingSprees", None)
        self.kills = kwargs.pop("kills", None)
        self.largest_killing_spree = kwargs.pop("largestKillingSpree", None)
        self.largest_multi_kill = kwargs.pop("largestMultiKill", None)
        self.longest_time_spent_living = kwargs.pop("longestTimeSpentLiving", None)
        self.magic_damage_dealt = kwargs.pop("magicDamageDealt", None)
        self.magic_damage_dealt_to_champions = kwargs.pop(
            "magicDamageDealtToChampions", None
            )
        self.magic_damage_taken = kwargs.pop("magicDamageTaken", None)
        self.penta_kills = kwargs.pop("pentaKills", None)
        self.physical_damage_dealt = kwargs.pop("physicalDamageDealt", None)
        self.physical_damage_dealt_to_champions = kwargs.pop(
            "physicalDamageDealtToChampions", None
            )
        self.physical_damage_taken = kwargs.pop("physicalDamageTaken", None)
        self.quadra_kills = kwargs.pop("quadraKills", None)
        self.spell1_casts = kwargs.pop("spell1Casts", None)
        self.spell2_casts = kwargs.pop("spell2Casts", None)
        self.spell3_casts = kwargs.pop("spell3Casts", None)
        self.spell4_casts = kwargs.pop("spell4Casts", None)
        self.summoner_spell1_casts = kwargs.pop("summoner1Casts", None)
        self.summoner_spell2_casts = kwargs.pop("summoner2Casts", None)
        self.time_CCing = kwargs.pop("timeCCingOthers", None)
        self.time_played = kwargs.pop("timePlayed", None)
        self.total_damage_dealt = kwargs.pop("totalDamageDealt", None)
        self.total_damage_dealt_to_champions = kwargs.pop(
            "totalDamageDealtToChampions", None
            )
        self.total_shielded_on_teammates = kwargs.pop(
            "totalDamageShieldedOnTeammates", None
            )
        self.total_damage_taken = kwargs.pop("totalDamageTaken", None)
        self.total_heal = kwargs.pop("totalHeal", None)
        self.total_heals_on_teammates = kwargs.pop("totalHealsOnTeammates", None)
        self.total_minions_killed = kwargs.pop("totalMinionsKilled", None)
        self.total_time_CC_dealt = kwargs.pop("totalTimeCCDealt", None)
        self.total_time_spent_dead = kwargs.pop("totalTimeSpentDead", None)
        self.triple_kills = kwargs.pop("tripleKills", None)
        self.true_damage_dealt = kwargs.pop("trueDamageDealt", None)
        self.true_damage_dealt_to_champions = kwargs.pop(
            "trueDamageDealtToChampions", None
            )
        self.true_damage_taken = kwargs.pop("trueDamageTaken", None)
        self.turret_kills = kwargs.pop("turretKills", None)
        self.turrets_lost = kwargs.pop("turretsLost", None)
        self.win = kwargs.pop("win", None)
        self.team_key = kwargs.pop("teamId")

        super().__call__(**kwargs)
        return self

class MatchCore(CoreObject):
    _dto_type = MatchDto
    _renamed = {
        "gameMode": "mode",
        "gameType" : "type",
        "gameName": "name",
        "queueId" : "queue",
        "platformId": "platform",
        "gameDuration": "duration"
    }

    def __call__(self, **kwargs):
        if "gameCreation" in kwargs:
            self.creation = kwargs["gameCreation"]/1000
        if "gameStartTimestamp" in kwargs:
            self.start = kwargs["gameStartTimestamp"]/1000
        if "gameEndTimestamp" in kwargs:
            self.end = kwargs["gameEndTimestamp"]/1000
        self.endedEarlySurrender = kwargs["participants"][0]["gameEndedInEarlySurrender"]
        version = kwargs["gameVersion"]
        self.version = match_version_to_version(version)
        self.version_id = version_to_id(version)

        participants = kwargs.pop("participants", [])
        self.participants = []
        for participant in participants:
            participant = ParticipantCore(
                **participant
            )
            self.participants.append(participant)
        
        super().__call__(**kwargs)

class MatchHistory(PoroGhost):
    _core_types = {MatchListCore}

    def __init__(
            self,
            continent: Continent,
            puuid: str,
            start: int = None,
            count: int = None
    ):
        kwargs = {"continent":continent,
                  "puuid":puuid}

        if start is not None:
            kwargs["start"] = start
            kwargs["count"] = count
        super().__init__(**kwargs)
    
    @property
    def match_ids(self) -> list:
        return self._data[MatchListCore].match_ids
    
    @property
    def continent(self) -> str:
        return self._data[MatchListCore].continent
    
    @property
    def puuid(self) -> str:
        return self._data[MatchListCore].puuid
    
    @property
    def count(self) -> int:
        return self._data[MatchListCore].count

class Participant(PoroGhost):
    _core_types={ParticipantCore}

    @classmethod
    def from_data(cls, data: CoreObject, match: "Match"):
        self = super().from_data(data)
        self._match = match
        return self

class Match(PoroGhost):
    _core_types={MatchCore}

    def __init__(
            self,
            region: Union[Region, str] = None,
            continent: Union[Continent, str] = None,
            id: str = None
    ):
        kwargs = {}

        if region is not None:
            if isinstance(region, str):
                region = Region(region.upper())
            kwargs["continent"] = region.continent
        elif continent is not None:
            if isinstance(continent, str):
                continent = Continent(continent)
            kwargs["continent"] = continent
        kwargs["id"] = id

        self._participants = []        
        super().__init__(**kwargs)
        
    
    @property
    def id(self) -> str:
        return self._data[MatchCore].id
    
    @property
    def version(self) -> str:
        return self._data[MatchCore].version
    
    @property
    def version_id(self) -> str:
        return self._data[MatchCore].version_id
    
    @property
    def continent(self) -> Continent:
        return Continent(self._data[MatchCore].continent)
    
    @property
    def creation(self) -> int:
        return self._data[MatchCore].creation
    
    @property
    def duration(self) -> int:
        return self._data[MatchCore].duration
    
    @property
    def start(self) -> int:
        return self._data[MatchCore].start
    
    @property
    def end(self) -> int:
        return self._data[MatchCore].end

    @property
    def endedEarlySurrender(self) -> bool:
        return self._data[MatchCore].endedEarlySurrender
    
    @property
    def participants(self) -> list[Participant]:
        print(len(self._participants))
        if len(self._participants)==0:
            for p in self._data[MatchCore].participants:
                participant = Participant.from_data(p, match=self)
                self._participants.append(participant)
        
        return list(self._participants)