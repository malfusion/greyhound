FROM bde2020/spark-base:3.0.0-hadoop3.2

LABEL maintainer="Gezim Sejdiu <g.sejdiu@gmail.com>, Giannis Mouchakis <gmouchakis@gmail.com>"

COPY worker.sh /

RUN pip3 install --upgrade pip
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install psycopg2


ENV SPARK_WORKER_WEBUI_PORT 8081
ENV SPARK_WORKER_LOG /spark/logs
ENV SPARK_MASTER "spark://spark-master:7077"



EXPOSE 8081

CMD ["/bin/bash", "/worker.sh"]
