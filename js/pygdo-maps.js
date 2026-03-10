"use strict";
window.gdo.maps = {
    gdo_init: function() {
        console.log('maps initied');
        window.gdo.maps.tracker.start();
        window.gdo.onlineMap,gdo_init();
    },

    tracker: mapsTracker(),


};
