from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
import psycopg2
import json

spark = SparkSession \
    .builder \
    .appName("KafkaTracesConsumer") \
    .getOrCreate()

span_df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "spans") \
  .load()

class SpanWriter:
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
            self.postgres_insert_start_time_query = """
                INSERT INTO spans (span_id, parent_span_id, process_id, cont_id, start_time, tags)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (span_id) DO UPDATE 
                SET start_time = %s;
            """
            self.postgres_insert_end_time_query = """
                INSERT INTO spans (span_id, parent_span_id, process_id, cont_id, end_time, tags)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (span_id) DO UPDATE 
                SET end_time = %s;
            """
            return True
        except Exception as error:
            print("ERROR:", error)

    def process(self, row):
        rowjson = json.loads(row.value.decode('utf-8'))
        spanType = None
        if 'end_time' in rowjson:
            spanType = 'end'
        elif 'start_time' in rowjson:
            spanType = 'start'
            
        record_to_insert = (
            rowjson['span_id'], 
            rowjson['parent_span_id'], 
            rowjson['process_id'], 
            rowjson['cont_id'], 
            rowjson['start_time'] if spanType=='start' else rowjson['end_time'], 
            rowjson['tags'],
            rowjson['start_time'] if spanType=='start' else rowjson['end_time']
            )
        if spanType == 'start':
            self.cursor.execute(self.postgres_insert_start_time_query, record_to_insert)
        if spanType == 'end':
            self.cursor.execute(self.postgres_insert_end_time_query, record_to_insert)

        self.connection.commit()

    def close(self, error):
        if(self.connection):
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")


res = span_df.writeStream.foreach(SpanWriter()).start()

# res = query \
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()

res.awaitTermination()
