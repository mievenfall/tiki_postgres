import json
from pathlib import Path
import psycopg2
from config import load_config

LAB_DIR = Path(__file__).resolve().parent
DATA_DIR = LAB_DIR.parent / "project2" / "tiki_crawl" / "output"

def load_json_files():
    product_files = sorted(DATA_DIR.glob("products_*.json"))
    if not product_files:
        raise FileNotFoundError(f"No products_*.json files found in: {DATA_DIR}")

    products = []
    for file_path in product_files:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        products.extend(data)
        print(f"Read {file_path.name}: {len(data)} products")

    return products

def prepare_rows(products):
    return [
        (
            product.get("id"),
            product.get("name"),
            product.get("url_key"),
            product.get("price"),
            product.get("description"),
            product.get("images_url") or [],
        )
        for product in products
    ]

def insert_products(rows, batch_size=1000):
    sql = """
    INSERT INTO products (
        id,
        name,
        url_key,
        price,
        description,
        images_url
    )
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    try:
        with psycopg2.connect(**load_config()) as conn:
            with conn.cursor() as cur:

                total = len(rows)

                for start in range(0, total, batch_size):
                    batch = rows[start:start + batch_size]

                    cur.executemany(sql, batch)
                    conn.commit()

                    end = start + len(batch)

                    print(
                        f"Inserted {end}/{total} products"
                    )

        print("Finished loading products.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def main():
    print(f"Reading JSON files from: {DATA_DIR}")
    products = load_json_files()
    print(f"\nTotal products read: {len(products)}")
    insert_products(prepare_rows(products))

if __name__ == "__main__":
    main()
