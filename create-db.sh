clickhouse-client --query "CREATE DATABASE IF NOT EXISTS perftest"

clickhouse-client --query "CREATE TABLE perftest.exchange_data (exchg_time_stamp DateTime,LMWI Decimal64(2),CJHA Decimal64(2),BCTD Decimal64(2),DNUL Decimal64(2),HEQB Decimal64(2),AOGT Decimal64(2),ELHW Decimal64(2),QIMJ Decimal64(2),ADFI Decimal64(2),EIWV Decimal64(2),IGXG Decimal64(2),HRCS Decimal64(2),PLFI Decimal64(2),QYUY Decimal64(2),SNUM Decimal64(2),WRBA Decimal64(2),UOFC Decimal64(2)) ENGINE = MergeTree() PARTITION BY toYYYYMM(exchg_time_stamp) ORDER BY (exchg_time_stamp)"
