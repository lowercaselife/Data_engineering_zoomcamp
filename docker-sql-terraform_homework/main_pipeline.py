import pandas as pd
from sqlalchemy import create_engine
import os

def main():
    user = os.getenv('PG_USER')
    password = os.getenv('PG_PASSWORD')
    host = os.getenv('PG_HOST')
    port = os.getenv('PG_PORT')
    db = os.getenv('PG_DB')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Green Taxi (Parquet)
    green_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
    print("Downloading Green Taxi data...")
    

    df_green = pd.read_parquet(green_url)
    
    chunk_size = 10000
    first = True

    print(f"Ingesting Green Taxi data in chunks of {chunk_size}...")
    for i in range(0, len(df_green), chunk_size):
        df_chunk = df_green.iloc[i : i + chunk_size]
        
        if first:
            # Create table with no data (replace existing)
            df_chunk.head(0).to_sql(name="green_taxi_trips", con=engine, if_exists="replace", index=False)
            first = False
            print("Table 'green_taxi_trips' created")

        # Insert chunk
        df_chunk.to_sql(name="green_taxi_trips", con=engine, if_exists="append", index=False)
        print(f"Inserted rows {i} to {min(i + chunk_size, len(df_green))}")

    #Taxi Zones (CSV)
    zone_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
    print("\nDownloading Zone data...")
    

    df_iter = pd.read_csv(zone_url, chunksize=100)
    first = True

    for df_chunk in df_iter:
        if first:
            df_chunk.head(0).to_sql(name="taxi_zones", con=engine, if_exists="replace", index=False)
            first = False
            print("Table 'taxi_zones' created")

        df_chunk.to_sql(name="taxi_zones", con=engine, if_exists="append", index=False)
        print(f"Inserted {len(df_chunk)} rows into taxi_zones")

    print("\nAll ingestions complete!")

if __name__ == "__main__":
    main()