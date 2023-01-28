
from enum import Enum
from urllib.parse import urljoin

class Lang(str, Enum):
    EN = 'en'
    
    def __str__(self) -> str:
        return str(self.value)

BASE_ROUTE = 'https://api.ambr.top/v2/'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'referer': 'https://ambr.top/'
}


ATTRIBUTETEXT = {
    "FIGHT_PROP_BASE_HP": "Base HP",
    "FIGHT_PROP_HP": "HP",
    "FIGHT_PROP_HP_PERCENT": "HP",
    "FIGHT_PROP_BASE_ATTACK": "Base ATK",
    "FIGHT_PROP_ATTACK": "ATK",
    "FIGHT_PROP_ATTACK_PERCENT": "ATK",
    "FIGHT_PROP_BASE_DEFENSE": "Base DEF",
    "FIGHT_PROP_DEFENSE": "DEF",
    "FIGHT_PROP_DEFENSE_PERCENT": "DEF",
    "FIGHT_PROP_BASE_SPEED": "Movement SPD",
    "FIGHT_PROP_SPEED_PERCENT": "Movement SPD",
    "FIGHT_PROP_CRITICAL": "CRIT Rate",
    "FIGHT_PROP_ANTI_CRITICAL": "CRIT RES",
    "FIGHT_PROP_CRITICAL_HURT": "CRIT DMG",
    "FIGHT_PROP_ELEMENT_MASTERY": "Elemental Mastery",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "Energy Recharge",
    "FIGHT_PROP_ADD_HURT": "DMG Bonus",
    "FIGHT_PROP_SUB_HURT": "DMG Reduction",
    "FIGHT_PROP_HEAL_ADD": "Healing Bonus",
    "FIGHT_PROP_HEALED_ADD": "Incoming Healing Bonus",
    "FIGHT_PROP_FIRE_ADD_HURT": "Pyro DMG Bonus",
    "FIGHT_PROP_FIRE_SUB_HURT": "Pyro RES",
    "FIGHT_PROP_WATER_ADD_HURT": "Hydro DMG Bonus",
    "FIGHT_PROP_WATER_SUB_HURT": "Hydro RES",
    "FIGHT_PROP_GRASS_ADD_HURT": "Dendro DMG Bonus",
    "FIGHT_PROP_GRASS_SUB_HURT": "Dendro RES",
    "FIGHT_PROP_ELEC_ADD_HURT": "Electro DMG Bonus",
    "FIGHT_PROP_ELEC_SUB_HURT": "Electro RES",
    "FIGHT_PROP_ICE_ADD_HURT": "Cryo DMG Bonus",
    "FIGHT_PROP_ICE_SUB_HURT": "Cryo RES",
    "FIGHT_PROP_WIND_ADD_HURT": "Anemo DMG Bonus",
    "FIGHT_PROP_WIND_SUB_HURT": "Anemo RES",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "Physical DMG Bonus",
    "FIGHT_PROP_PHYSICAL_SUB_HURT": "Physical RES",
    "FIGHT_PROP_ROCK_ADD_HURT": "Geo DMG Bonus",
    "FIGHT_PROP_ROCK_SUB_HURT": "Geo RES",
    "FIGHT_PROP_EFFECT_HIT": "Hit",
    "FIGHT_PROP_EFFECT_RESIST": "Resisted",
    "FIGHT_PROP_FREEZE_SHORTEN": "Frozen Duration Reduction",
    "FIGHT_PROP_TORPOR_SHORTEN": "Paralyzed Duration Reduction",
    "FIGHT_PROP_DIZZY_SHORTEN": "Stunned Duration Reduction",
    "FIGHT_PROP_MAX_HP": "Max HP",
    "FIGHT_PROP_CUR_ATTACK": "ATK",
    "FIGHT_PROP_CUR_DEFENSE": "DEF",
    "FIGHT_PROP_CUR_SPEED": "Movement SPD",
    "FIGHT_PROP_CUR_HP": "HP",
    "FIGHT_PROP_SKILL_CD_MINUS_RATIO": "CD Reduction",
    "FIGHT_PROP_SHIELD_COST_MINUS_RATIO": "Shield Strength",
    "WEAPON_NONE": "Unknown Weapon",
    "WEAPON_CROSSBOW": "Crossbow",
    "WEAPON_STAFF": "Staff",
    "WEAPON_DOUBLE_DAGGER": "Dual Blades",
    "WEAPON_KATANA": "Katana",
    "WEAPON_SHURIKEN": "Shuriken",
    "WEAPON_STICK": "Rod",
    "WEAPON_SPEAR": "Polearm",
    "WEAPON_SHIELD_SMALL": "Buckler",
    "WEAPON_CATALYST": "Catalyst",
    "WEAPON_CLAYMORE": "Claymore",
    "WEAPON_BOW": "Bow",
    "WEAPON_POLE": "Polearm",
    "FIGHT_PROP_ATTACK_PERCENT_A": "ATK Percentage",
    "FIGHT_PROP_DEFENSE_PERCENT_A": "DEF Percentage",
    "FIGHT_PROP_HP_PERCENT_A": "HP Percentage",
    "WEAPON_SWORD": "Sword"
}