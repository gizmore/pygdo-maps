from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDO_User import GDO_User
from gdo.maps.GDT_Lat import GDT_Lat
from gdo.maps.GDT_Lng import GDT_Lng


class track(Method):
    """
    Track a user.
    """

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def gdo_needs_authentication(self) -> bool:
        return True

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_Lat('lat'),
            GDT_Lng('lng'),
        ]

    def gdo_execute(self) -> GDT:
        self.gdo_module().track_position(
            GDO_User.current(),
            self.param_val('lat'),
            self.param_val('lng'),
        )
        return self.empty()
