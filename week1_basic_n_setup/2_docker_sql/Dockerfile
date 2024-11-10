FROM python:3.9.1

ENV URL=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 pyarrow fastparquet

WORKDIR /app
COPY parquet_to_csv.py parquet_to_csv.py
COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py" ]
