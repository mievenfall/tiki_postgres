import json
from pathlib import Path

import psycopg2

from config import load_config


LAB_DIR = Path(__file__).resolve().parent

DATA_DIR = (
    LAB_DIR.parent
    / "project2"
    / "tiki_crawl"
    / "output"
)


def load_json_files():
    product_files = sorted(DATA_DIR.glob("products_*.json"))

    if not product_files:
        raise FileNotFoundError(
            f"No products_*.json files found in: {DATA_DIR}"
        )

    products = []

    for file_path in product_files:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        products.extend(data)

        print(
            f"Read {file_path.name}: "
            f"{len(data)} products"
        )

    return products


def prepare_rows(products):
    rows = []

    for product in products:
        rows.append(
            (
                product.get("id"),
                product.get("name"),
                product.get("url_key"),
                product.get("price"),
                product.get("description"),
                product.get("images_url") or [],
            )
        )

    return rows


def load_products(rows, batch_size=1000):
    check_sql = """
        SELECT id
        FROM products
        WHERE id = %s;
    """

    insert_sql = """
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

    update_sql = """
        UPDATE products
        SET
            name = %s,
            url_key = %s,
            price = %s,
            description = %s,
            images_url = %s
        WHERE id = %s;
    """

    config = load_config()

    inserted = 0
    updated = 0
    processed = 0

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                total = len(rows)

                for row in rows:
                    product_id = row[0]

                    cur.execute(
                        check_sql,
                        (product_id,)
                    )

                    exists = cur.fetchone()

                    if exists:
                        cur.execute(
                            update_sql,
                            (
                                row[1],
                                row[2],
                                row[3],
                                row[4],
                                row[5],
                                product_id,
                            ),
                        )

                        updated += 1

                    else:
                        cur.execute(
                            insert_sql,
                            row,
                        )

                        inserted += 1

                    processed += 1

                    if processed % batch_size == 0:
                        conn.commit()

                        print(
                            f"Processed {processed}/{total} "
                            f"| inserted={inserted} "
                            f"| updated={updated}"
                        )

                conn.commit()

                print(
                    f"Processed {processed}/{total} "
                    f"| inserted={inserted} "
                    f"| updated={updated}"
                )

        print("\nFinished loading products.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def main():
    print(
        f"Reading JSON files from: {DATA_DIR}"
    )

    products = load_json_files()

    print(
        f"\nTotal products read: {len(products)}"
    )

    rows = prepare_rows(products)

    load_products(rows)


if __name__ == "__main__":
    main()
