from gdo.core.GDT_Enum import GDT_Enum
from gdo.base.Trans import t


class GDT_TrackMode(GDT_Enum):

    PRECISE = 'precise'
    BLURRED = 'blurred'
    MANUAL = 'manual'

    def __init__(self, name: str):
        super().__init__(name)
        self.not_null()
        self.icon('select')

    def gdo_choices(self) -> dict:
        return {
            self.PRECISE: t(self.PRECISE),
            self.BLURRED: t(self.BLURRED),
            self.MANUAL: t(self.MANUAL),
        }
