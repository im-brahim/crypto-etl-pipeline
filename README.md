# Crypto ETL Pipeline with Airflow and Spark

This project is an end-to-end **ETL pipeline** designed to fetch cryptocurrency prices from a public API, process the data using **Apache Spark**, and save the results to a **PostgreSQL** database, all orchestrated by **Apache Airflow**.
<!-- Additionally, **Jupyter Notebooks** are used for interactive data exploration. -->

## Architecture

- **Airflow**: Used for orchestrating the ETL workflow and scheduling tasks.
- **Spark**: Used for processing the raw cryptocurrency data and saving it in a structured format.
- **MinIO**: Acts as an S3-compatible storage solution for storing raw and processed data.
- **PostgreSQL**: Data storage for processed cryptocurrency prices.
<!-- - **Jupyter**: Provides an interactive environment for analyzing the data with Spark. -->

## Technologies

- Apache Airflow
- Apache Spark
- MinIO (S3 storage)
- PostgreSQL
<!-- - Jupyter -->
- Docker

## How to Run Locally

1. Clone this repository:

   ```bash
   git clone https://github.com/im-brahim/crypto-etl-pipeline.git
   cd crypto-etl-pipeline

2. Make sure Docker is running, and then start the services:

    ```bash
    docker-compose up

3. Once the containers are up and running, you can access:

- Airflow at http://localhost:8081

- Spark Master UI at http://localhost:8080

<!-- - Jupyter at http://localhost:8888 -->

4. The DAG files for Airflow are located in the /dags/ folder, where each DAG performs a specific ETL task.

### Notes:

<!-- **Jupyter:** Jupyter notebooks are included in this setup to provide an interactive environment for exploring the processed data, running Spark jobs, and performing additional analysis. You can access Jupyter by navigating to http://localhost:8888. -->

**Docker Compose:** The entire stack is managed using Docker Compose, which simplifies the process of running all services (Airflow, Spark, MinIO, PostgreSQL, and Jupyter) locally.

## How the ETL Process Works

1. **Fetching Data**:
The crypto_price_hourly.py DAG fetches cryptocurrency prices (Bitcoin and Ethereum) from the CoinGecko API and saves them as JSON in MinIO.

2. **Processing Data**:
The process_crypto.py Spark job reads the data from MinIO, flattens the JSON, and saves the processed data in Parquet format.

3. **Saving Data to PostgreSQL**:
The save_to_db.py script saves the processed data to a PostgreSQL database for storage and analysis.

## 🔄 Pipeline Steps

1. **Fetch** cryptocurrency data from an external API
2. **Store** raw data as JSON in MinIO
3. **Process** data using Spark
4. **Save** transformed data to PostgreSQL
5. **Automate** everything via Airflow DAG

## How to Stop the Services
To stop the services once you're done, run the following command: 
    
      ```bash
      docker-compose down

## Skills Practiced

- Data orchestration with Airflow

- Spark ETL pipeline

- Object storage via MinIO

- Docker-based data platform

- Python scripting for real-world ETL

## !!!Important Notes on jars Folder and Drivers!!!
The jars folder contains essential drivers for integration with PostgreSQL and MinIO. Specifically:

- PostgreSQL JDBC Driver: postgresql-42.6.0.jar

- MinIO S3 Connector: hadoop-aws-3.3.4.jar, aws-java-sdk-1.12.262.jar

These files are not included in the repository due to size constraints. Please download the following versions and place them in the jars/ folder.

### 💡 About The Project: 

This project was developed as a learning exercise with the help of ChatGPT AI to simulate a real-world data engineering project.

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

### 🤝 AI Collaboration

- I used ChatGPT to:
  - Guide my architecture decisions
  - Explain difficult topics step-by-step
  - Troubleshoot errors and refine ideas
  - Act as a coach throughout the entire project

---

_This was more than just coding — it was a deep learning experience._ 🚀
