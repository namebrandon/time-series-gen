time (for filename in data/*.csv; do
                clickhouse-client \
                    --query="INSERT INTO perftest.exchange_data FORMAT CSV" < $filename
        done)