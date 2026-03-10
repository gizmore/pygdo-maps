"use strict";

window.gdo.onlineMap = {



    map: null,
    playerMarker: null,

    gdo_init: function() {
        this.map = L.map('map', {
            center: [52.52, 13.405], // Berlin default
            zoom: 14,
        });

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(this.map);

        this.hookClicks();
        this.locatePlayer();
    },

    hookClicks: function() {
        this.map.on('click', (e) => {
            const {lat, lng} = e.latlng;
            console.log('clicked', lat, lng);
            this.spawnMob(lat, lng);
        });
    },

    locatePlayer: function() {
        navigator.geolocation.getCurrentPosition((pos) => {
            const lat = pos.coords.latitude;
            const lng = pos.coords.longitude;

            this.map.setView([lat, lng], 16);

            this.playerMarker = L.marker([lat, lng])
                .addTo(this.map)
                .bindPopup("You are here")
                .openPopup();
        });
    },

    spawnMob: function(lat, lng) {
        L.circle([lat, lng], {
            radius: 20,
        }).addTo(this.map);
    }
};
