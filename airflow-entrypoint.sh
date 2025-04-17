#!/bin/bash

airflow db migrate
airflow users create \
  --username admin \
  --firstname admin \
  --lastname admin \
  --role Admin \
  --email admin@example.com \
  --password admin

airflow scheduler &

exec airflow webserver