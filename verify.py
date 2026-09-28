import psycopg2
from config import load_config

def verify():
    try:
        with psycopg2.connect(**load_config()) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM products;")
                print(f"Products in PostgreSQL: {cur.fetchone()[0]}")

                cur.execute("SELECT id, name, price FROM products LIMIT 5;")
                print("\nSample rows:")
                for row in cur.fetchall():
                    print(row)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == "__main__":
    verify()
