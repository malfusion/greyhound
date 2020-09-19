FROM bde2020/spark-base:3.0.0-hadoop3.2

COPY template.sh /
RUN pip3 install --upgrade pip
RUN apk add postgresql-dev gcc python3-dev musl-dev

# Copy the requirements.txt first, for separate dependency resolving and downloading
COPY requirements.txt /app/

RUN pip3 install pyspark
RUN apk add zip

RUN cd /app && pip3 install -r requirements.txt

# Copy the source code
COPY . /app

ENV SPARK_MASTER_NAME spark-master
ENV SPARK_MASTER_PORT 7077
ENV SPARK_APPLICATION_PYTHON_LOCATION /app/entrypoint.py

# ENV SPARK_APPLICATION_JAR_LOCATION /app/application.jar
# ENV SPARK_APPLICATION_MAIN_CLASS my.main.Application

ENV SPARK_APPLICATION_ARGS ""

COPY submit.sh /

CMD ["/bin/bash", "/submit.sh"]
