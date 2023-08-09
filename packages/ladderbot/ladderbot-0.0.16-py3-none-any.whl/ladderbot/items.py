class Weapon:
    def __init__(self, weapon_popup_element, overlay_stats) -> None:
        self.name = ""
        self.rarity = ""
        self.bonus_level = overlay_stats[0]
        self.tier = overlay_stats[1]
        self.type = "weapon"
        self.level_req = 0
        self.stats = []
        self.min_damage = 0
        self.max_damage = 0
        self.parse_weapon(weapon_popup_element)
    def __repr__(self) -> str:
        return f"<Weapon {self.name}>"
    def parse_weapon(self, weapon_popup_element) -> list:
        weapon_stats = [stat.strip() for stat in weapon_popup_element.text.split('\n')]
        self.name = weapon_stats[0]
        rarities = ["magical","rare","mystical","angelic","mythical","arcane","legendary","godly","epic","relic","artifact","unique"]
        rarity = self.name.split()[0].lower()
        if rarity in rarities:
            self.rarity = rarity
        else:
            self.rarity = 'plain'
        for stat in weapon_stats[1:]:
            if "level req:" in stat.lower():
                self.level_req = int(stat.split(' ')[-1])
            if "damage:" in stat.lower():
                self.min_damage, self.max_damage = [int(num) for num in stat.split(' ') if num.isdigit()]
            if "+" in stat.lower():
                self.stats.append(stat.lower())
#-----------------------------------------------
class Armor:
    def __init__(self, armor_popup_element, overlay_stats) -> None:
        self.name = ""
        self.rarity = ""
        self.bonus_level = overlay_stats[0]
        self.tier = overlay_stats[1]
        self.type = "armor"
        self.level_req = 0
        self.stats = []
        self.min_phys_defense = 0
        self.max_phys_defense = 0
        self.min_mag_defense = 0
        self.max_mag_defense = 0
        self.parse_armor(armor_popup_element)
    def __repr__(self) -> str:
        return f"<Armor {self.name}>"
    def parse_armor(self, armor_popup_element) -> list:
        armor_stats = [stat.strip() for stat in armor_popup_element.text.split('\n')]
        self.name = armor_stats[0]
        rarities = ["magical","rare","mystical","angelic","mythical","arcane","legendary","godly","epic","relic","artifact","unique"]
        rarity = self.name.split()[0].lower()
        if rarity in rarities:
            self.rarity = rarity
        else:
            self.rarity = 'plain'
        for stat in armor_stats[1:]:
            if "level req" in stat.lower():
                self.level_req = int(stat.split(' ')[-1])
            if "physical defense" in stat.lower():
                self.min_phys_defense, self.max_phys_defense = [int(num) for num in stat.split(' ') if num.isdigit()]
            if "magic defense" in stat.lower():
                self.min_mag_defense, self.max_mag_defense = [int(num) for num in stat.split(' ') if num.isdigit()]
            if "+" in stat:
                self.stats.append(stat)
#-----------------------------------------------
class Charm:
    def __init__(self, charm_popup_element, overlay_stats) -> None:
        self.name = ""
        self.rarity = ""
        self.bonus_level = overlay_stats[0]
        self.tier = overlay_stats[1]
        self.type = "charm"
        self.level_req = 0
        self.stats = []
        self.min_spell_effect = 0
        self.max_spell_effect = 0
        self.mana_cost = 0
        self.parse_charm(charm_popup_element)
    def __repr__(self) -> str:
        return f"<Charm {self.name}>"
    def parse_charm(self, charm_popup_element) -> list:
        charm_stats = [stat.strip() for stat in charm_popup_element.text.split('\n')]
        self.name = charm_stats[0]
        rarities = ["magical","rare","mystical","angelic","mythical","arcane","legendary","godly","epic","relic","artifact","unique"]
        rarity = self.name.split()[0].lower()
        if rarity in rarities:
            self.rarity = rarity
        else:
            self.rarity = 'plain'
        for stat in charm_stats[1:]:
            if "level req" in stat.lower():
                self.level_req = int(stat.split(' ')[-1])
            if "spell damage" in stat.lower() or "heals" in stat.lower():
                self.min_spell_effect, self.max_spell_effect = [int(num) for num in stat.split(' ') if num.isdigit()]
            if "mana cost" in stat.lower():
                self.mana_cost = int(stat.split(':')[-1].strip())
            if "+" in stat.lower():
                self.stats.append(stat.lower())
#-----------------------------------------------
