#!/bin/bash

mkdir -p tmp
# Insert 1000 subscribers
for i in {132..100031}
do
    imsistr=$(printf "%010d" $i)
    imsi=20895$imsistr
    echo "Inserting subscriber $imsi"
    echo "('${imsi}', '5G_AKA', '0C0A34601D4F07677303652C0462535B', '0C0A34601D4F07677303652C0462535B', '{\\\"sqn\\\": \\\"000000000020\\\", \\\"sqnScheme\\\": \\\"NON_TIME_BASED\\\", \\\"lastIndexes\\\": {\\\"ausf\\\": 0}}', '8000', 'milenage', '63bfa50ee6523365ff14c1f45f88737d', NULL, NULL, NULL, NULL, '${imsi}')," >> tmp/subs.sql
done