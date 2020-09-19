from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
import psycopg2
import json

spark = SparkSession \
    .builder \
    .appName("KafkaTracesConsumer") \
    .getOrCreate()

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "traces") \
  .load()

class ForeachWriter:
    def open(self, partition_id, epoch_id):
        try:
            print("PostgreSQL connection is starting")
            self.connection = psycopg2.connect(user="postgres",
                                            password="postgres",
                                            host="postgres",
                                            port="5432",
                                            database="postgres")
            print("PostgreSQL connection is started")
            self.cursor = self.connection.cursor()
            self.postgres_insert_query = """ INSERT INTO traces (model, price) VALUES (%s,%s)"""
            return True
        except Exception as error:
            print("ERROR:", error)

    def process(self, row):
        rowjson = json.loads(row.value.decode('utf-8'))
        record_to_insert = (rowjson['somekey'], 950)
        self.cursor.execute(self.postgres_insert_query, record_to_insert)
        self.connection.commit()

    def close(self, error):
        if(self.connection):
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")

res = df.writeStream.foreach(ForeachWriter()).start()

# res = query \
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()

res.awaitTermination()
