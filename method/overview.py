from gdo.base.GDT import GDT
from gdo.ui.MethodPage import MethodPage


class overview(MethodPage):

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def gdo_parameters(self) -> list[GDT]:
        return []

    def form_submitted(self):
        return self.msg('%s', 'Yeah!')

