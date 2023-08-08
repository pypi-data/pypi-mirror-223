import handler
from desc import Desc


class Town:
    def __init__(self, town_name):
        town_data = handler.get_data(town_name)

        self.fillcolor = town_data["fillcolor"]
        self.ytop = town_data["ytop"]
        self.color = town_data["color"]
        self.markup = town_data["markup"]
        self.x = town_data["x"]
        self.weight = town_data["weight"]
        self.z = town_data["z"]
        self.ybottom = town_data["ybottom"]
        self.label = town_data["label"]
        self.opacity = town_data["opacity"]
        self.fillopacity = town_data["fillopacity"]
        self.desc = Desc(town_data)

    def fillcolor(self):
        return self.fillcolor

    def ytop(self):
        return self.ytop

    def color(self):
        return self.ytop

    def markup(self):
        return self.markup

    def x(self):
        return self.x

    def weight(self):
        return self.weight

    def z(self):
        return self.z

    def ybottom(self):
        return self.ybottom

    def label(self):
        return self.label

    def opacity(self):
        return self.opacity

    def fillopacity(self):
        return self.fillopacity

    def desc(self):
        return self.desc
