from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split





spark = SparkSession \
    .builder \
    .appName("KafkaTracesConsumer") \
    .getOrCreate()

spark.sparkContext.addPyFile("dependencies.zip")
import psycopg2


df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "traces") \
  .load()

# query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

class ForeachWriter:
    def open(self, partition_id, epoch_id):
        
        try:
            self.connection = psycopg2.connect(user="postgres",
                                            password="postgres",
                                            host="postgres",
                                            port="5432",
                                            database="postgres")
            self.cursor = connection.cursor()
            self.postgres_insert_query = """ INSERT INTO traces (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
            
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Failed to insert record into mobile table", error)


    def process(self, row):
        print("HERERERE")
        print(row)
        record_to_insert = (1, row['somekey'], 950)
        self.cursor.execute(self.postgres_insert_query, record_to_insert)
        connection.commit()

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
