from __future__ import annotations

from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Util import Files
from gdo.core.GDT_UInt import GDT_UInt
from gdo.date.GDT_Duration import GDT_Duration
from gdo.maps.GDO_UserPos import GDO_UserPos
from gdo.maps.GDT_Lat import GDT_Lat
from gdo.maps.GDT_Lng import GDT_Lng
from gdo.maps.GDT_TrackMode import GDT_TrackMode
from gdo.ui.GDT_Link import GDT_Link

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gdo.ui.GDT_Page import GDT_Page


class module_maps(GDO_Module):

    def gdo_classes(self) -> list[type[GDO]]:
        return [
            GDO_UserPos,
        ]

    async def gdo_install(self):
        Files.copy_dir(self.file_path('node_modules/leaflet/dist/images/'), self.assets_path('images/'))

    def gdo_licenses(self) -> list[str]:
        return [
            'node_modules/leaflet/LICENSE',
        ]

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_Duration('ping_interval').initial('2m 30s').min(10).max(72800).not_null(),
            GDT_UInt('default_tracking_digits').initial('3').min(0).max(9).not_null(),
            GDT_TrackMode('default_tracking_mode').initial(GDT_TrackMode.BLURRED),
        ]

    def cfg_default_digits(self) -> str:
        return self.get_config_val('default_tracking_digits')

    def cfg_default_mode(self) -> str:
        return self.get_config_val('default_tracking_mode')

    def gdo_user_config(self) -> list[GDT]:
        return [
            GDT_Lat('last_latitude').tooltip('tt_last_latitude'),
            GDT_Lng('last_longitude').tooltip('tt_last_longitude'),
        ]

    def gdo_user_settings(self) -> list[GDT]:
        return [
            GDT_TrackMode('map_tracking').initial(self.cfg_default_mode()).label('tracking_mode').tooltip('tt_map_tracking'),
            GDT_UInt('map_track_digits').min(0).max(9).initial(self.cfg_default_digits()).label('tracking_digits').tooltip('tt_map_tracking_digits'),
        ]

    def gdo_init(self):
        # Files.copy_dir(self.file_path('node_modules/leaflet/dist/images/'), self.assets_path('images/'))
        pass

    def gdo_load_scripts(self, page: 'GDT_Page'):
        self.add_bower_js('leaflet/dist/leaflet-src.js')
        self.add_bower_css('leaflet/dist/leaflet.css')
        self.add_js('js/pygdo-maps.js')
        self.add_css('css/pygdo-maps.css')

    def gdo_init_sidebar(self, page: 'GDT_Page'):
        page._left_bar.add_field(GDT_Link().href(self.href('overview')).text('module_maps'))
