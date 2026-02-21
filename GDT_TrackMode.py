from gdo.core.GDT_Enum import GDT_Enum


class GDT_TrackMode(GDT_Enum):

    PRECISE = 'precise'
    BLURRED = 'blurred'
    MANUAL = 'manual'

    def __init__(self, name: str):
        super().__init__(name)
        self.not_null()

    def gdo_choices(self) -> dict:
        return {
            self.PRECISE: self.PRECISE,
            self.BLURRED: self.BLURRED,
            self.MANUAL: self.MANUAL,
        }
