mongo world_data --eval "db.dropDatabase()" 


"C:\Program Files\MongoDB\Server\3.4\bin\mongoimport"  --db world_data --collection airports       --type json --file "C:\data\world\airports_fixed.geojson"    --jsonArray


"C:\Program Files\MongoDB\Server\3.4\bin\mongoimport"  --db world_data --collection countries      --type json --file "C:\data\world\countries.geojson"            --jsonArray


"C:\Program Files\MongoDB\Server\3.4\bin\mongoimport"  --db world_data --collection meteorites     --type json --file "C:\data\world\meteorite_fixed.geojson"   --jsonArray


"C:\Program Files\MongoDB\Server\3.4\bin\mongoimport"  --db world_data --collection volcanos       --type json --file "C:\data\world\volcanos_fixed.geojson"      --jsonArray


"C:\Program Files\MongoDB\Server\3.4\bin\mongoimport"  --db world_data --collection earthquakes    --type json --file "C:\data\world\earthquakes_fixed.geojson"          --jsonArray


"C:\Program Files\MongoDB\Server\3.4\bin\mongoimport"  --db world_data --collection cities         --type json --file "C:\data\world\world_cities_fixed.geojson "        --jsonArray


"C:\Program Files\MongoDB\Server\3.4\bin\mongoimport"  --db world_data --collection states         --type json --file "C:\data\world\state_borders.geojson"        --jsonArray



"C:\Program Files\MongoDB\Server\3.4\bin\mongoimport"  --db world_data --collection terrorism         --type json --file "C:\data\world\globalterrorism_fixed.geojson"        --jsonArray