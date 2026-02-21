from gdo.base.GDT import GDT
from gdo.core.GDT_Composite import GDT_Composite
from gdo.maps.GDT_Lat import GDT_Lat
from gdo.maps.GDT_Lng import GDT_Lng


class GDT_GeoPos(GDT_Composite):

    def __init__(self, name: str):
        super().__init__(name)

    def gdo_components(self) -> list['GDT']:
        return [
            GDT_Lat(self._name + "_lat"),
            GDT_Lng(self._name + "_lng"),
        ]
