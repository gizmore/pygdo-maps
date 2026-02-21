from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDO_User import GDO_User
from gdo.maps.GDO_UserPos import GDO_UserPos
from gdo.maps.GDT_Lat import GDT_Lat
from gdo.maps.GDT_Lng import GDT_Lng


class track(Method):
    """
    Track a user.
    """

    def gdo_needs_authentication(self) -> bool:
        return True

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_Lat('lat'),
            GDT_Lng('lng'),
        ]

    def gdo_execute(self) -> GDT:
        GDO_UserPos.blank({
            'up_user': GDO_User.current().get_id(),
            'up_pos_lat': self.param_val('lat'),
            'up_pos_lng': self.param_val('lng'),
        }).soft_replace()
        return self.empty()
