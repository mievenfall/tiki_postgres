# Lab 1 - Load Tiki JSON Data into PostgreSQL

## DoD

Use Python to read all Tiki product data from Project 02 and load it into PostgreSQL.

---

## Folder Structure

`project2` and `lab1` are sibling folders:

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
    ├── delete_products.py
    ├── verify.py
    ├── requirements.txt
    ├── .gitignore
    └── README.md
```

The loader reads source data from:

```text
../project2/tiki_crawl/output/
```

---

## Data Flow

```text
products_*.json
       ↓
open/read file
       │
       ↓
    parse JSON
       │
       ↓
prepare product data
       │
       ↓
connect to PostgreSQL
       │
       ↓
SELECT product by id
       │
    ┌──┴──┐
    ↓     ↓
exist    not exists
    │     │
    ↓     ↓
UPDATE   INSERT
       ↓
     commit
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

`images_url` is stored as PostgreSQL `TEXT[]` because the source field is a Python list of image URLs.

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

`database.ini` should not be committed to Git.

---

## Create the Table

Run:

```bash
python3 create_tables.py
```

Expected output:

```text
Created products table.
```

---

## Load Product Data

Run:

```bash
python3 load_products.py
```

The script:

1. Reads every `products_*.json` file from Project 02.
2. Converts each product into a Python tuple.
3. Checks whether the product `id` already exists in PostgreSQL.
4. Uses `INSERT` for new products.
5. Uses `UPDATE` for existing products.
6. Commits progress in batches.

This prevents duplicate rows because `id` is the primary key and existing products are updated instead of inserted again.

Example progress:

```text
Processed 1000/124299 | inserted=1000 | updated=0
Processed 2000/124299 | inserted=2000 | updated=0
...
```

If the script is run again, existing products are updated:

```text
Processed 1000/124299 | inserted=0 | updated=1000
...
```

---

## Verify the Load

Run:

```bash
python3 verify.py
```

Expected row count for the current Project 02 output:

```text
Products in PostgreSQL: 124299
```

The script also prints sample rows from the `products` table.

---

## Delete All Product Data

To remove all rows while keeping the table itself:

```bash
python3 delete_products.py
```

The script uses:

```sql
DELETE FROM products;
```

and reports the number of deleted rows.

Example:

```text
Deleted 124299 products.
```

After deletion:

```bash
python3 verify.py
```

should return:

```text
Products in PostgreSQL: 0
```

---

## Python Files

### `config.py`

Loads PostgreSQL connection settings from `database.ini`.

### `create_tables.py`

Connects to PostgreSQL and creates the `products` table.

### `load_products.py`

Reads all Project 02 JSON files and loads them into PostgreSQL using:

```text
SELECT -> INSERT or UPDATE
```

### `verify.py`

Checks the number of rows in the table and prints sample data.

### `delete_products.py`

Deletes all rows from `products` using Python and SQL `DELETE`.

---

## Concepts Practiced

This lab focuses on the Python/PostgreSQL workflow:

- connect to PostgreSQL with `psycopg2`
- create tables
- execute SQL with a cursor
- query data with `SELECT`
- insert data with `INSERT`
- modify existing data with `UPDATE`
- remove data with `DELETE`
- commit transactions
- read query results with `fetchone()` and `fetchall()`
