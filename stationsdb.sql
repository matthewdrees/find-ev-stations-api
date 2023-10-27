CREATE TABLE stations (
    coordinates point NOT NULL,
    name text NOT NULL,
    address text NOT NULL,
    city_state_zip text NOT NULL,
    access_days_time text,
    ev_network text,
    ev_network_web text,
    dc_fast_chargers smallint,
    ev_level_1_chargers smallint,
    ev_level_2_chargers smallint,
    ev_connector_types text
);

INSERT INTO stations VALUES( point(-122.3493,47.6205), 'Space Needle', '400 Broad St',
    'Seattle, WA 98109', '24 hours', 'Space needle', 'https://www.spaceneedle.com/',
    0, 1, 2, 'J1772');

COPY stations FROM '/tmp/stations.csv'; 

EXPLAIN ANALYZE SELECT *
FROM stations
ORDER BY POINT(-122.3493,47.6205) <-> coordinates
LIMIT 20;

--                                                          QUERY PLAN
-- ----------------------------------------------------------------------------------------------------------------------------
--  Limit  (cost=5129.29..5129.34 rows=20 width=163) (actual time=30.057..30.060 rows=20 loops=1)
--    ->  Sort  (cost=5129.29..5274.60 rows=58126 width=163) (actual time=30.055..30.057 rows=20 loops=1)
--          Sort Key: (('(-122.3493,47.6205)'::point <-> coordinates))
--          Sort Method: top-N heapsort  Memory: 34kB
--          ->  Seq Scan on stations  (cost=0.00..3582.58 rows=58126 width=163) (actual time=0.008..12.517 rows=58126 loops=1)
--  Planning Time: 0.069 ms
--  Execution Time: 30.084 ms
-- (7 rows)

CREATE INDEX coordinates_idx on stations USING gist(coordinates);
VACUUM ANALYZE stations;

--                                                                 QUERY PLAN
-- -------------------------------------------------------------------------------------------------------------------------------------------
--  Limit  (cost=0.28..5.10 rows=20 width=163) (actual time=0.394..0.415 rows=20 loops=1)
--    ->  Index Scan using coordinates_idx on stations  (cost=0.28..14006.80 rows=58126 width=163) (actual time=0.393..0.412 rows=20 loops=1)
--          Order By: (coordinates <-> '(-122.3493,47.6205)'::point)
--  Planning Time: 0.700 ms
--  Execution Time: 0.644 ms
-- (5 rows)

DROP INDEX coordinates_idx;
CREATE INDEX coordinates_idx on stations USING spgist(coordinates);
VACUUM ANALYZE stations;

--                                                                 QUERY PLAN
-- -------------------------------------------------------------------------------------------------------------------------------------------
--  Limit  (cost=0.28..5.07 rows=20 width=163) (actual time=0.141..0.162 rows=20 loops=1)
--    ->  Index Scan using coordinates_idx on stations  (cost=0.28..13938.80 rows=58126 width=163) (actual time=0.139..0.159 rows=20 loops=1)
--          Order By: (coordinates <-> '(-122.3493,47.6205)'::point)
--  Planning Time: 0.255 ms
--  Execution Time: 0.246 ms
-- (5 rows)
