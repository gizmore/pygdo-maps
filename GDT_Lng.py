from gdo.core.GDT_Decimal import GDT_Decimal


class GDT_Lng(GDT_Decimal):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.icon('position')
        self.label('longitude')
        self.digits(3, 9)
        self.max(180)
        self.min(-180)
