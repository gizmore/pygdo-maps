from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Index import GDT_Index
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created
from gdo.maps.GDT_GeoPos import GDT_GeoPos


class GDO_UserPos(GDO):

    def gdo_table_engine(self) -> str:
        return 'MEMORY'

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('up_id'),
            GDT_User('up_user').not_null(),
            GDT_GeoPos('up_pos').not_null(),
            GDT_Created('up_created'),
            GDT_Index('up_idx_user_created').index_fields('up_user', 'up_created'),
        ]
