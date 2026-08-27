from gdo.base.GDT import GDT
from gdo.base.Method import Method


class ping(Method):
    """Accept the browser's tracking heartbeat; Maps handles its geo header."""

    def gdo_needs_authentication(self) -> bool:
        return False

    def gdo_execute(self) -> GDT:
        return self.empty()
