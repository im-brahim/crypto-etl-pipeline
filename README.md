# 🔁 End-to-End ETL Pipeline with Spark, Airflow, MinIO & PostgreSQL

This project is a complete local ETL (Extract, Transform, Load) pipeline designed to simulate a production-like data engineering environment using Docker Compose.

The pipeline fetches live cryptocurrency data from an API, processes it using Apache Spark, stores it in MinIO (S3-compatible object storage), and finally loads the transformed data into a PostgreSQL database.

---

## 🧱 Tech Stack

- **Apache Spark 3.5.0** – For distributed data processing
- **Apache Airflow 2.7.2** – For DAG orchestration
- **MinIO** – For object storage (S3-compatible)
- **PostgreSQL** – As the final storage layer
- **Docker Compose** – For service orchestration
- **Python** – For job scripts

---

## ⚙️ Features

- 🌐 Fetches crypto price data from a public API
- 🔄 Runs ETL jobs on a schedule using Airflow
- 🚀 Spark reads from MinIO and writes to PostgreSQL
- 🐳 Fully containerized for portability

---

## 🚀 Getting Started

### 1. Clone the repo
    
    ```bash
    git clone https://github.com/your-username/data-pipeline-etl.git
    cd data-pipeline-etl

### 2. Start all services
    
    ```bash
    docker-compose up --build

### 3. Open Airflow

- Navigate to http://localhost:8081

- Enable and trigger the DAG spark_etl_pipeline

## 📂 Project Structure

    .
    ├── dags/                  # Airflow DAGs
    ├── jobs/                  # Spark job scripts
    ├── jars/                  # AWS & PostgreSQL JDBC drivers
    ├── data/                  # Optional data output
    ├── docker-compose.yml     # Service orchestration
    └── README.md 

### 🚫 !!!Important Notes on jars Folder and Drivers!!!

The jars folder contains essential drivers for integration with PostgreSQL and MinIO. Specifically:

- PostgreSQL JDBC Driver: postgresql-42.6.0.jar

- MinIO S3 Connector: hadoop-aws-3.3.4.jar, aws-java-sdk-1.12.262.jar

These files are not included in the repository due to size constraints. Please download the following versions and place them in the jars/ folder.

## 💡 Notes

This project was developed for practice purposes to simulate an end-to-end ETL workflow. The analysis part was tested separately but is not included in this repo.

### 🤝 AI Collaboration

Built with the help of AI (ChatGPT) for coding assistant 👨‍🏫
- I used ChatGPT to:
  - Guide my architecture decisions
  - Explain difficult topics step-by-step
  - Troubleshoot errors and refine ideas

---

### 🧩 Why I Did This

- To simulate a **real-world data pipeline**
- To gain hands-on practice with:
  - Apache Spark
  - Apache Airflow
  - Docker Compose
  - MinIO (object storage)
  - PostgreSQL
  - Python & ETL scripting

### 🛠️ What I Built

- A full pipeline that:
  - Fetches crypto data from an API
  - Stores raw data in MinIO
  - Transforms it using Spark
  - Loads it into a PostgreSQL database
  - Is orchestrated end-to-end with Airflow

### 🧠 What I Learned

- How to set up a **modular Spark cluster** in Docker
- How to build **reliable Airflow DAGs**
- How to manage **volumes and file paths** in containerized systems
- How to debug common issues (JDBC, BashOperator vs DockerOperator, file mounts)
- How to think like a **data engineer** when building pipelines

_This was more than just coding — it was a deep learning experience._ 🚀