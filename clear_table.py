import psycopg2

from config import load_config


def delete_all_products():
    sql = "DELETE FROM products;"

    rows_deleted = 0

    try:
        config = load_config()

        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

                rows_deleted = cur.rowcount

            conn.commit()

        print(f"Deleted {rows_deleted} products.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == "__main__":
    delete_all_products()
