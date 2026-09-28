## DoD

Use Python to read all Tiki product data from Project 02 and load it into PostgreSQL.

---

## Folder Structure

This lab assumes `project2` and `lab1` are sibling folders:

```text
Desktop/
├── project2/
│   └── tiki_crawl/
│       └── output/
│           ├── products_001.json
│           ├── products_002.json
│           └── ...
│
└── lab1/
    ├── config.py
    ├── database.ini.example
    ├── create_tables.py
    ├── load_products.py
    ├── verify.py
    ├── requirements.txt
    ├── .gitignore
    ├── README.md
    ├── scripts/
    │   └── run.sh
    └── logs/
```

The loader reads source data from:

```text
../project2/tiki_crawl/output/
```

---

## Data Flow

```text
project2/tiki_crawl/output/products_*.json
                    ↓
              Python json.load()
                    ↓
             prepare tuples
                    ↓
       insert in batches of 1000
                    ↓
          psycopg2.executemany()
                    ↓
               PostgreSQL
                    ↓
               products
```

---

## PostgreSQL Table

```sql
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name TEXT,
    url_key TEXT,
    price BIGINT,
    description TEXT,
    images_url TEXT[]
);
```

`images_url` is stored as a PostgreSQL `TEXT[]` because the source field is a list of image URLs.

---

## Setup

### 1. Open Lab 1

```bash
cd ~/Desktop/lab1
```

### 2. Create and activate the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

```bash
sudo -u postgres psql
```

Inside PostgreSQL:

```sql
CREATE DATABASE lab1;
```

Exit:

```text
\\q
```

### 5. Create the local database config

```bash
cp database.ini.example database.ini
nano database.ini
```

Example:

```ini
[postgresql]
host=localhost
database=lab1
user=postgres
password=YOUR_PASSWORD
port=5432
```

`database.ini` is ignored by Git.

---

## Create the Table

```bash
python3 create_tables.py
```

Expected output:

```text
Created products table.
```

---

## Load All Product Data

The loader reads every `products_*.json` file from:

```text
~/Desktop/project2/tiki_crawl/output/
```

The current Project 02 output contains:

```text
124299 products
```

To avoid one very large transaction, the loader inserts products in batches of 1000 rows and commits after each batch.

Example progress:

```text
Inserted 1000/124299 products
Inserted 2000/124299 products
...
Inserted 124299/124299 products
Finished loading products.
```

---

## Run with Bash Logging

Instead of running `load_products.py` directly, use:

```bash
chmod +x scripts/run.sh
./scripts/run.sh
```

The Bash script:

- activates the local `venv`
- runs `load_products.py`
- displays output in the terminal
- saves both stdout and stderr to a log file
- records start time, finish time, runtime, and exit code

Logs are written to:

```text
logs/load_products_YYYYMMDD_HHMMSS.log
```

Example:

```text
========================================
LAB 1 - TIKI JSON -> POSTGRESQL
========================================
Started at: 2026-09-28 01:23:45
Project dir: /home/eve/Desktop/lab1
Log file: /home/eve/Desktop/lab1/logs/load_products_20260928_012345.log
========================================

Reading JSON files from: /home/eve/Desktop/project2/tiki_crawl/output
...
Total products read: 124299

Inserted 1000/124299 products
...
Inserted 124299/124299 products
Finished loading products.

========================================
LAB 1 FINISHED
========================================
Runtime: 00:xx:xx
Exit code: 0
========================================
```

---

## Verify the Load

After the loader finishes:

```bash
python3 verify.py
```

Expected row count:

```text
Products in PostgreSQL: 124299
```

The script also prints a few sample rows.

---

## Important Notes

The current loader uses standard `INSERT` statements and `cursor.executemany()` to stay close to the PostgreSQL Python tutorial.

Because `id` is the primary key, running the full loader again against an already populated table will cause duplicate-key errors.

For this lab, the intended workflow is:

```text
create database
      ↓
create table
      ↓
load data once
      ↓
verify
```


