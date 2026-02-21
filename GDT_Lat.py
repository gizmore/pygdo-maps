from gdo.core.GDT_Decimal import GDT_Decimal


class GDT_Lat(GDT_Decimal):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.icon('position')
        self.label('latitude')
        self.digits(2, 9)
        self.max(90)
        self.min(-90)

