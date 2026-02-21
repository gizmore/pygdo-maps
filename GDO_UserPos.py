from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created
from gdo.maps.GDT_GeoPos import GDT_GeoPos


class GDO_UserPos(GDO):

    def gdo_table_engine(self) -> str:
        return 'MEMORY'

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_User('up_user').primary(),
            GDT_GeoPos('up_pos').not_null(),
            GDT_Created('up_created'),
        ]
