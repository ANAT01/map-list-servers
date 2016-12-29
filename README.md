# Map server's list

## Build parameters

### make build

> Build data sources for QuickMapServices (Qgis plugin)

> Result been locate in **build/** folder

### make test

> Build data sources for QuickMapServices (Qgis plugin)

> Result been locate in **build/** folder

> Files in **~/.qgis2/python/plugins/quick_map_services/** been replaced from builded sources



---
providers:
  - 
      type: tms
      name:
        en: Yandex Satelite
        ru: Яндекс Спутник
      url: "[mirrors].maps.yandex.net/tiles?l=sat&x={x}&y={y}&z={z}"
      mirrors: sat01, sat02, sat03, sat04
      tag: color, satelite
      srs: "+proj=merc +a=6378137 +b=6356752 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs"
      z_min: 0
      z_max: 20
      y_origin_top: true
  -
      type: tms
      name:
        en: Yandex Map
        ru: Яндекс Карта
      url: "wvec.maps.yandex.net/?l=wmap&x={x}&y={y}&z={z}"
      tag: color, map
      srs: "+proj=merc +a=6378137 +b=6356752 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs"
      z_min: 0
      z_max: 20
      y_origin_top: true
legal_policy:
  rights: BY-NC-ND (https://en.wikipedia.org/wiki/Creative_Commons_license)
  license: PTY (https://en.wikipedia.org/wiki/Software_license)
  copyright: Яндекс
  termofuse: https://legal.yandex.ru/maps_termsofuse/?lang=ru
