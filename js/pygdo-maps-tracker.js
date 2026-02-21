/**
 * Geopos header injector for every request:
 * - fetch() (native + monkeypatch)
 * - XMLHttpRequest
 *
 * Header name: X-Geo-Pos
 * Value: "lat,lon;acc=<meters>;ts=<ms>"
 * If no permission/position: "na"
 */
function mapsTracker() {
  const HEADER = "X-Geo-Pos";
  let last = null; // {lat, lon, acc, ts}
  let watchId = null;

  function encode(pos) {
    if (!pos) return "na";
    const lat = Number(pos.lat).toFixed(9);
    const lon = Number(pos.lon).toFixed(9);
    const acc = pos.acc != null ? Math.round(pos.acc) : "";
    const ts = pos.ts != null ? Math.round(pos.ts) : Date.now();
    return `${lat},${lon};acc=${acc};ts=${ts}`;
  }

  function setLastFromGeolocation(geoPos) {
    last = {
      lat: geoPos.coords.latitude,
      lon: geoPos.coords.longitude,
      acc: geoPos.coords.accuracy,
      ts: geoPos.timestamp || Date.now(),
    };
  }

  async function getPosHeaderValue() {
    // fresh enough? (10s)
    if (last && Date.now() - last.ts < 10_000) return encode(last);

    // try a single shot if not watching
    if (!("geolocation" in navigator)) return "na";

    try {
      const geoPos = await new Promise((resolve, reject) =>
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          maximumAge: 10_000,
          timeout: 1500,
        })
      );
      setLastFromGeolocation(geoPos);
      return encode(last);
    } catch (_) {
      return "na";
    }
  }

  function addHeaderToHeaders(headers, value) {
    try {
      if (headers instanceof Headers) {
        if (!headers.has(HEADER)) headers.set(HEADER, value);
        return headers;
      }
      if (Array.isArray(headers)) {
        // [ [k,v], ... ]
        if (!headers.some(([k]) => String(k).toLowerCase() === HEADER.toLowerCase())) {
          headers.push([HEADER, value]);
        }
        return headers;
      }
      if (headers && typeof headers === "object") {
        const has = Object.keys(headers).some((k) => k.toLowerCase() === HEADER.toLowerCase());
        if (!has) headers[HEADER] = value;
        return headers;
      }
    } catch (_) {}
    // fallback
    const h = new Headers(headers || {});
    if (!h.has(HEADER)) h.set(HEADER, value);
    return h;
  }

  function installFetchPatch() {
    if (!window.fetch) return;
    const origFetch = window.fetch.bind(window);

    window.fetch = async function (input, init) {
      init = init || {};
      const value = await getPosHeaderValue();
      init.headers = addHeaderToHeaders(init.headers, value);
      return origFetch(input, init);
    };
  }

  function installXhrPatch() {
    if (!window.XMLHttpRequest) return;

    const origOpen = XMLHttpRequest.prototype.open;
    const origSend = XMLHttpRequest.prototype.send;
    const origSet = XMLHttpRequest.prototype.setRequestHeader;

    XMLHttpRequest.prototype.open = function (...args) {
      this.__gdoGeoHeaderSet = false;
      return origOpen.apply(this, args);
    };

    XMLHttpRequest.prototype.setRequestHeader = function (k, v) {
      if (String(k).toLowerCase() === HEADER.toLowerCase()) {
        this.__gdoGeoHeaderSet = true;
      }
      return origSet.apply(this, arguments);
    };

    XMLHttpRequest.prototype.send = function (body) {
      if (this.__gdoGeoHeaderSet) return origSend.apply(this, arguments);

      // async header injection, then continue send()
      getPosHeaderValue()
        .then((value) => {
          try {
            origSet.call(this, HEADER, value);
          } catch (_) {}
          origSend.call(this, body);
        })
        .catch(() => origSend.call(this, body));

      // prevent immediate send; we call it above
      return;
    };
  }

  function install() {
    installFetchPatch();
    installXhrPatch();
  }

  function startWatching() {
    if (!("geolocation" in navigator)) return;
    if (watchId != null) return;

    watchId = navigator.geolocation.watchPosition(
      (geoPos) => setLastFromGeolocation(geoPos),
      (_) => {},
      { enableHighAccuracy: true, maximumAge: 10_000, timeout: 10_000 }
    );
  }

  function stopWatching() {
    if (!("geolocation" in navigator)) return;
    if (watchId == null) return;
    navigator.geolocation.clearWatch(watchId);
    watchId = null;
  }

  // install immediately
  install();

  return {
    start: startWatching,
    stop: stopWatching,
    get headerName() {
      return HEADER;
    },
    get last() {
      return last;
    },
  };
}