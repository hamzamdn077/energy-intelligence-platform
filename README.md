# energy-intelligence-platform

pulls US electricity generation data from the EIA API and transforms it into an analytics-ready model on Databricks. bronze → silver → gold, PySpark for ingestion and cleaning, dbt for modeling.

## structure

```
databricks/
  ingest_eia.py           # EIA API → bronze ADLS
  silver_electricity.py   # PySpark cleaning → silver Delta

energy/                   # dbt project
  models/
    staging/
    intermediate/
    gold/                 # dim_date, dim_location, fct_electricity_generation
  seeds/
    fuel_categories.csv

src/energy_project/
pyproject.toml
```

## setup

store your EIA API key as a Databricks secret (`scope=autkey`, `key=eia-API`), then:

```bash
uv sync
cd energy && dbt seed && dbt run && dbt test
```

run the Databricks notebooks before dbt.

## data source

[EIA Electric Power Operational Data](https://www.eia.gov/opendata/)
