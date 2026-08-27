import os
import unittest

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.maps.module_maps import module_maps
from gdo.maps.GDO_UserPos import GDO_UserPos
from gdo.maps.GDT_TrackMode import GDT_TrackMode
from gdotest.TestUtil import cli_plug, reinstall_module, cli_gizmore, GDOTestCase, WebPlug, install_module, web_plug


class module_maps_Test(GDOTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        install_module('maps')
        loader.load_modules_db(True)
        WebPlug.COOKIES = {}
        Application.init_cli()
        loader.init_modules(True, True)
        loader.init_cli()

    def test_00_reinstall(self):
        reinstall_module('maps')
        self.assertIs(type(module_maps.instance()), module_maps, "Cannot re-install module maps.")

    def test_03_overview_cli(self):
        giz =  cli_gizmore()
        out = cli_plug(giz, "$maps.overview")
        self.assertIsNotNone(out, '$maps.overview does not work.')

    def test_02_overview_web(self):
        giz =  cli_gizmore()
        out = web_plug("maps.overview.html")
        self.assertIsNotNone(out, 'maps.overview.html does not work.')

    def test_04_tracks_a_valid_geo_header(self):
        user = cli_gizmore()
        user.save_setting('map_tracking', 'blurred')
        user.save_setting('map_track_digits', '2')
        self.assertTrue(module_maps.instance().track_header(
            user, '52.123456789,10.987654321;acc=12;ts=123'
        ))
        position = GDO_UserPos.table().select().where(f'up_user={user.get_id()}').first().exec().fetch_object()
        self.assertEqual(52.12, float(position.gdo_val('up_pos_lat')))
        self.assertEqual(10.99, float(position.gdo_val('up_pos_lng')))
        self.assertEqual('52.12', user.get_setting_val('last_latitude'))
        self.assertEqual('10.99', user.get_setting_val('last_longitude'))

        module_maps.instance().track_header(user, '52.129,10.991')
        positions = GDO_UserPos.table().select().where(f'up_user={user.get_id()}').exec().fetch_all()
        self.assertEqual(2, len(positions))

    def test_05_does_not_track_manual_or_invalid_headers(self):
        user = cli_gizmore()
        user.save_setting('map_tracking', 'manual')
        self.assertFalse(module_maps.instance().track_header(user, '52.1,10.2'))
        self.assertFalse(module_maps.instance().track_header(user, 'not-a-position'))

    def test_06_renders_translated_tracking_modes(self):
        field = GDT_TrackMode('map_tracking')
        self.assertEqual('Save exact', field.display_val(GDT_TrackMode.PRECISE))

    def test_07_accepts_the_tracking_ping(self):
        self.assertIsNotNone(web_plug('maps.ping.json'))


if __name__ == '__main__':
    unittest.main()
