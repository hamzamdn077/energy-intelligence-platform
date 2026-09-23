# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

# COMMAND ----------

bronze_path = "abfss://bronze@energstorageacc.dfs.core.windows.net/electricity/"
silver_path = "abfss://silver@energstorageacc.dfs.core.windows.net/electricity/"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Bronze

# COMMAND ----------

bronze_path = "abfss://bronze@energstorageacc.dfs.core.windows.net/electricity/"
df = spark.read \
    .option("multiLine", True) \
    .option("recursiveFileLookup", "true") \
    .json(bronze_path)
print("Bronze records:", df.count())

# COMMAND ----------

df = df.select(
    F.explode("response.data").alias("data")
)

df = df.select("data.*")

# COMMAND ----------

display(df.limit(10))

# COMMAND ----------

df = df.select(
    F.col("period").alias("period"),
    F.col("location").alias("location"),
    F.col("stateDescription").alias("state_description"),
    F.col("sectorid").alias("sector_id"),
    F.col("sectorDescription").alias("sector_description"),
    F.col("fueltypeid").alias("fuel_type_id"),
    F.col("fuelTypeDescription").alias("fuel_type_description"),
    F.col("generation").cast(DoubleType()).alias("generation"),
    F.col("generation-units").alias("generation_units")
)

# COMMAND ----------

df = df.withColumn(
    "period",
    F.to_date(F.concat(F.col("period"), F.lit("-01")))
)

# COMMAND ----------

df = df.dropDuplicates([
    "period",
    "location",
    "sector_id",
    "fuel_type_id"
])

# COMMAND ----------

df = df.filter(
    F.col("generation").isNotNull()
)

# COMMAND ----------

df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save(silver_path)

# COMMAND ----------

print("Silver data written successfully.")
print("Silver records:", df.count())


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM delta.`abfss://silver@energstorageacc.dfs.core.windows.net/electricity/`
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS energy;
# MAGIC CREATE SCHEMA IF NOT EXISTS energy.silver;
# MAGIC CREATE TABLE energy.silver.electricity
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://silver@energstorageacc.dfs.core.windows.net/electricity/';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM energy.silver.electricity
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS energy.gold;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN energy;

# COMMAND ----------

