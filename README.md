# Big Data Engineering — NTI Labs & Projects

This repository hosts a comprehensive suite of laboratory exercises, assignments, and architectural implementations completed as part of the **Big Data Engineering Program** at the **National Telecommunication Institute (NTI)**.

Developed by **Ali Mersal** ([ali.m.mersal@gmail.com](mailto:ali.m.mersal@gmail.com)).

---

## 📖 Abstract

Modern big data engineering requires a solid grasp of distributed storage, parallel execution frameworks, and NoSQL databases. This repository serves as a centralized portfolio demonstrating practical proficiency across the entire Apache Hadoop ecosystem and Apache Spark.

The project ranges from the fundamentals of **HDFS** partition schemes and cluster architecture to building custom **MapReduce** Python streaming jobs for large-scale text and server log analysis. It includes advanced distributed querying through **Apache HBase** and **Apache Hive** integration, as well as scalable data pipelines and window analytics leveraging **PySpark**. To top it off, a desktop administration dashboard (**Hadoop Control Center Ultimate UI**) was built using Python Tkinter to simplify the deployment, monitoring, and interaction with local HDFS clusters.

---

## 🛠️ Technology Stack

* **Distributed Storage**: Apache HDFS (Hadoop Distributed File System)
* **Resource Management**: Apache YARN (Yet Another Resource Negotiator)
* **NoSQL Database**: Apache HBase (Columnar distributed database)
* **Data Warehousing**: Apache Hive & HBase-Hive Integration
* **Data Processing & Analytics**: Apache Spark (PySpark), Python MapReduce Streaming (Mapper/Reducer)
* **User Interface & Tooling**: Python Tkinter Desktop GUI, Jupyter Notebooks

---

## 📂 Repository Structure

The repository is logically organized by technology stack modules:

```text
├── HDFS/
│   ├── Task1-ali-mersal.pdf       # HDFS architecture configuration & reports
│   ├── final-diagram-hdfs.png     # Custom HDFS architecture workflow diagram
│   └── gui.py                     # Hadoop Control Center Ultimate GUI application
│
├── Hbase/
│   ├── HBase_Assignment.pdf       # NoSQL design, schema modeling & CLI exercises
│   ├── HBase_Student_Lab.pdf      # Detailed steps for HBase operations
│   └── HBase_Student_Lab- PART 2.pdf
│
├── Mapreduce/
│   ├── lab 1/                     # Basic Python MapReduce (e.g. Word Count)
│   ├── lab 2/                     # Data cleaning and filtering pipelines
│   ├── lab 3/                     # Server logs analyzer (Apache Web Log parsing)
│   └── lab 4/                     # Numerical aggregation and grouping jobs
│       ├── map.py                 # Streaming Mapper
│       ├── reduce.py              # Streaming Reducer
│       └── output/                # Job verification screenshots & outputs
│
├── Spark/
│   ├── PySpark_Lab1.pdf           # PySpark architectural foundation
│   └── PySpark_Student_Practice_Lab.ipynb  # Interactive Spark DataFrame & SQL exercises
│
└── hive/
    └── HBase & Hive Integration Case Study .pdf # Enterprise data integration guide
```

---

## 💻 Module Overviews

### 1. HDFS & Hadoop Control Center
* **HDFS Architecture**: Detailed analysis of NameNodes, DataNodes, Replication factors, and Write/Read pathways (`Task1-ali-mersal.pdf`).
* **Hadoop Control Center (`HDFS/gui.py`)**: A modern desktop application with:
  * One-click start/stop control for HDFS and YARN daemons.
  * Real-time service status checks (`jps`).
  * Direct filesystem explorer (browsing, uploading, downloading, and deleting files).
  * Direct path permission modifications (`chmod`).
  * Custom commands console with pre-loaded command templates.

### 2. Apache HBase
* Practical implementation of schema design for column-oriented databases.
* CRUD operations, table scans, row key optimization, and versioning control.

### 3. Python MapReduce Streaming
Contains 4 standalone labs simulating industrial batch processing using MapReduce streaming:
* **Lab 1**: Word occurrence frequency count.
* **Lab 2**: Substring scanning, cleaning, and record filtering.
* **Lab 3**: Processing raw Apache log records to count hits per client IP.
* **Lab 4**: Double-pass aggregation for numerical statistics (minimum, maximum, average values).

### 4. PySpark Analytics
An intensive practice notebook (`Spark/PySpark_Student_Practice_Lab.ipynb`) focusing on:
* **DataFrame APIs**: Selection, filters, schema-casting, and joins.
* **Conditional Logic**: `when().otherwise()` grading structures.
* **Window Functions**: Dynamic ranks, running totals, and partition sorting (`F.rank().over(windowSpec)`).
* **Complex Types**: Array manipulations, flattening (`F.explode()`), and string parsing/regex functions.

### 5. Hive & HBase Integration
* Structuring data warehouses on top of active HBase tables.
* Running SQL queries using Apache Hive that compile into underlying HBase scans, bridging the gap between transactional NoSQL databases and structured analytics.

---

## 🚀 Getting Started

### Running the Hadoop Control Center GUI
To use the GUI console, make sure you have python3 and `tkinter` installed on your Hadoop master machine:
```bash
# Install tkinter
sudo apt-get install python3-tk

# Run the control center
python HDFS/gui.py
```
> **Note**: Adjust the Hadoop installation paths inside the `Config` class of `gui.py` to point to your specific installation directory (Default is set to `/home/bigdata/hadoop-2.7.3`).

### Running MapReduce Jobs Locally
You can test the MapReduce streaming scripts locally without a full Hadoop cluster using:
```bash
cat dataset.txt | python map.py | sort | python reduce.py
```

---

## 📧 Contact & Info
* **Author**: Ali Mersal
* **Email**: [ali.m.mersal@gmail.com](mailto:ali.m.mersal@gmail.com)
* **Institution**: National Telecommunication Institute (NTI)
