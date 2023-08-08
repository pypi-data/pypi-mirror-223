import re


class Flags:
    def __init__(self, flags_dict):
        self.has_keepup = flags_dict["has Upkeep"]
        self.pvp = flags_dict["pvp"]
        self.mobs = flags_dict["mobs"]
        self.explosion = flags_dict["explosion"]
        self.fire = flags_dict["fire"]
        self.nation = flags_dict["nation"]
        self.ruined = flags_dict["ruined"]


class Desc:
    def __init__(self, town_data):
        desc = town_data["desc"]
        flags_dict = {}
        title_match = re.search(
            r"<span style=\"font-size:120%\">(.+?)<\/span>", desc)
        if title_match:
            self.title = title_match.group(1)
        mayor_match = re.search(
            r"Mayor <span style=\"font-weight:bold\">(.+?)<\/span>", desc)
        if mayor_match:
            self.mayor = mayor_match.group(1)
        associates_match = re.search(
            r"Associates <span style=\"font-weight:bold\">(.+?)<\/span>", desc)
        if associates_match:
            self.associates = [assoc.strip()
                               for assoc in associates_match.group(1).split(",")]
        flags_match = re.search(
            r"Flags<br /><span style=\"font-weight:bold\">(.+?)<\/span>", desc)
        if flags_match:
            flags_text = flags_match.group(1)
            flags_list = flags_text.split("<br />")
            for flag in flags_list:
                key, value = flag.split(":")
                flags_dict[key.strip()] = value.strip()
            self.flags = Flags(flags_dict)
