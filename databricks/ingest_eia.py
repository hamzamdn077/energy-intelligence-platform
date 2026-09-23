# Databricks notebook source
import requests
import json
from datetime import datetime

# COMMAND ----------

states = ["NY", "TX", "CA"]
start_date = "2026-01"
end_date = "2026-09"
api_key = dbutils.secrets.get(
    scope="autkey",
    key="eia-API"
)
base_url = "https://api.eia.gov/v2/electricity/electric-power-operational-data/data/"

# COMMAND ----------

for state in states:

    params = {
        "api_key": api_key,
        "frequency": "monthly",
        "data[0]": "generation",
        "facets[location][]": state,
        "start": start_date,
        "end": end_date
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(
            f"EIA request failed for {state}: {response.status_code}"
        )

    data = response.json()

    output_path = (
        f"abfss://bronze@energstorageacc.dfs.core.windows.net/electricity/"
        f"{state}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    dbutils.fs.put(
        output_path,
        json.dumps(data),
        overwrite=True
    )
    print(f"{state}: data saved")

# COMMAND ----------

