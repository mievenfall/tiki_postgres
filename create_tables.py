import psycopg2
from config import load_config

def create_tables():
    sql = """
    CREATE TABLE IF NOT EXISTS products (
        id BIGINT PRIMARY KEY,
        name TEXT,
        url_key TEXT,
        price BIGINT,
        description TEXT,
        images_url TEXT[]
    );
    """

    config = load_config()
    
    try:
	
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
        print("Created products table.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == "__main__":
    create_tables()
