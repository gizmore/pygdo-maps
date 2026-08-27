from __future__ import annotations

from gdo.base.Application import Application
from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDO_User import GDO_User
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

    GEO_HEADER = 'X-Geo-Pos'

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
            GDT_Duration('ping_interval').initial('1m').min(10).max(72800).not_null(),
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
        Application.EVENTS.subscribe('user_request', self.on_user_request)

    def on_user_request(self, user: GDO_User):
        """Persist the browser's latest position header for this HTTP request."""
        if not user.is_authenticated() or not user.is_persisted():
            return
        header = (
            Application.get_client_header('HTTP_X_GEO_POS') or
            Application.get_client_header(self.GEO_HEADER)
        )
        self.track_header(user, header)

    def track_header(self, user: GDO_User, header: str | None) -> bool:
        """Validate and apply the ``X-Geo-Pos`` value injected by the browser."""
        if not header or header.strip().lower() == 'na':
            return False
        try:
            coordinates = header.split(';', 1)[0].split(',', 1)
            latitude, longitude = (float(value.strip()) for value in coordinates)
        except (TypeError, ValueError):
            return False
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            return False

        mode = user.get_setting_val('map_tracking') or self.cfg_default_mode()
        if mode == GDT_TrackMode.MANUAL:
            return False
        digits = 9 if mode == GDT_TrackMode.PRECISE else int(
            user.get_setting_val('map_track_digits') or self.cfg_default_digits()
        )
        self.track_position(user, latitude, longitude, digits)
        return True

    def track_position(self, user: GDO_User, latitude: float | str, longitude: float | str, digits: int = 9) -> GDO_UserPos:
        """Append a waypoint and retain the latest position in user settings."""
        latitude = str(round(float(latitude), digits))
        longitude = str(round(float(longitude), digits))
        user.save_setting('last_latitude', latitude)
        user.save_setting('last_longitude', longitude)
        return GDO_UserPos.blank({
            'up_user': user.get_id(),
            'up_pos_lat': latitude,
            'up_pos_lng': longitude,
        }).insert()

    def gdo_load_scripts(self, page: 'GDT_Page'):
        self.add_bower_js('leaflet/dist/leaflet-src.js')
        self.add_bower_css('leaflet/dist/leaflet.css')
        self.add_js('js/pygdo-maps-tracker.js')
        self.add_js('js/pygdo-leaflet.js')
        self.add_js('js/pygdo-maps.js')
        self.add_css('css/pygdo-maps.css')

    def gdo_init_sidebar(self, page: 'GDT_Page'):
        page._left_bar.add_field(GDT_Link().href(self.href('overview')).text('module_maps'))
