# setup


Update different project databases with current data:
atlas_backend and atlas_meetbouten for now


   docker exec -it datapuntgeosearch_atlas_db_1 update-atlas.sh

   docker exec -it datapuntgeosearch_nap_db_1 update-nap.sh

pip install -r requirements.txt

test postgres spatial queries:

run python test_dataset.py



# Geospatial queries

Doel is zoeken op coordinaat door de (aangegeven) aanwezige database
views en features teruggeven aan de client in geojson formaat.

## Taal/framework keuze

Flask/SQLAlchemy

## Soorten queries
Er zijn twee soorten postgis queries van toepassing voor de usecase:

* ST_DWithin voor ST_Point velden
* ST_Contains voor ST_Polygon ST_MultiPolygon

We zoeken momenteel nog niet op ST_MultiLineString.

## RD/WGS84
Momenteel is de geometrie opgeslagen in RD srid. We zouden naast deze
kolom een kolom kunnen toevoegen waarin geometrie rsid WGS84 is. Met
deze rsid heeft kunnen we een ST_GeoHash index gebruiken in plaats van
de GEOS filter, wat beter performt.

View & index aanmaken wordt dan zoiets:

`CREATE MATERIALIZED VIEW {}_mat AS SELECT *, ST_Transform(geometrie,
4326) as geometrie_wgs84 FROM {}`

`CREATE INDEX {}_idx ON {}_mat USING GIST(geometrie)`

`GISTCREATE INDEX {}_idx_wgs84 ON {}_mat USING
ST_GeoHash(geometrie_wgs84)`geometrie_wgs84

# Elastic
Deze service bevat ook code voor het indexeren en zoeken via elastic
search. De impelemntatie is nog niet compleet en moet we op een latere
tijd opgepakt worden. Wat moet er nog gebeuren:

- Toestan van object functie als mapping waarde. Dit is om te
  ondersteunen, b.v. het maken van de naam eigenschaap als een
combinatie van een aantal model velden
- Toevoegen van link URL. De link url is via DjangoRestFramework en er
  moet implementatie komen voor het genereren van.
- Gebruik van verschillende indices in combinatie met aliases
- Support voor filtering gebaseerd op de indices used


