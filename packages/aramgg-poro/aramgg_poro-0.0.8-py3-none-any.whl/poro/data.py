from enum import Enum

class Region(Enum):
    brazil = "BR"
    europe_north_east = "EUNE"
    europe_west = "EUW"
    japan = "JP"
    korea = "KR"
    latin_america_north = "LAN"
    latin_america_south = "LAS"
    north_america = "NA"
    oceania = "OCE"
    turkey = "TR"
    russia = "RU"

    @property
    def continent(self) -> "Continent":
        if self is Region.brazil:
            return Continent.americas
        if self is Region.europe_north_east:
            return Continent.europe
        if self is Region.europe_west:
            return Continent.europe
        if self is Region.japan:
            return Continent.asia
        if self is Region.korea:
            return Continent.asia
        if self is Region.latin_america_north:
            return Continent.americas
        if self is Region.latin_america_south:
            return Continent.americas
        if self is Region.north_america:
            return Continent.americas
        if self is Region.oceania:
            return Continent.sea
        if self is Region.turkey:
            return Continent.europe
        if self is Region.russia:
            return Continent.europe

class Continent(Enum):
    americas = "AMERICAS"
    asia = "ASIA"
    europe = "EUROPE"
    sea = "SEA"