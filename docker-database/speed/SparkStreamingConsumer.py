from pymongo import MongoClient
from pyspark.sql import SparkSession
import time
import pandas as pd
import pymongo
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.streaming import StreamingContext
def push_to_cosmos(row):
    dict_row = row.asDict()
    client = MongoClient('mongodb://127.0.0.1:27017')
    database = client['poli']
    collection = database['polisites']
    collection.insert_one(dict_row)

schema = StructType([
    StructField("body", StringType(), True),
    StructField("title", StringType(), True)
])
spark = SparkSession \
    .builder \
    .appName("SSKafka")\
    .getOrCreate()

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "article") \
  .load()


kafka_df_string = df.selectExpr(["CAST(value as STRING)"])
tweets_table = kafka_df_string.select(from_json(col("value"), schema).alias("data")).select("data.*")
query = tweets_table.writeStream.format('json').foreach(push_to_cosmos).start()

query.awaitTermination()



"""
* Uit te voeren als volgt:
spark-submit --packages={{bin/kafka-installatie}}

spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0,org.mongodb.spark:mongo-spark-connector_2.11:2.4.0 SparkStreamingConsumer.py

"""
