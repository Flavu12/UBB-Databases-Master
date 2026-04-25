import psycopg2
from psycopg2.extras import execute_batch
from tqdm import tqdm
import random
import string
import time
import os

# === CONFIG ===
DB_NAME = "lab1_isgbd"
DB_USER = "postgres"
DB_PASS = "a"
DB_HOST = "localhost"
DB_PORT = "5432"

N_OWNERS = 5_000_000
N_PETS = 5_000_000
BATCH_SIZE = 50_000
CSV_FILE = "pet.csv"

def random_name():
    return ''.join(random.choices(string.ascii_lowercase, k=8))

def disable_safety_settings(curs):
    print("Disabling safety settings for bulk load...")
    curs.execute("ALTER SYSTEM SET synchronous_commit = off;")
    curs.execute("ALTER SYSTEM SET fsync = off;")
    curs.execute("ALTER SYSTEM SET full_page_writes = off;")

def enable_safety_settings(curs):
    print("Re-enabling safety settings...")
    curs.execute("ALTER SYSTEM RESET synchronous_commit;")
    curs.execute("ALTER SYSTEM RESET fsync;")
    curs.execute("ALTER SYSTEM RESET full_page_writes;")

def drop_indexes_and_constraints(curs):
    print("Dropping foreign key and indexes...")
    curs.execute("ALTER TABLE IF EXISTS pet DROP CONSTRAINT IF EXISTS pet_id_owner_fkey;")
    curs.execute("DROP INDEX IF EXISTS idx_pet_name;")
    curs.execute("DROP INDEX IF EXISTS idx_pet_owner_id;")
    curs.execute("DROP INDEX IF EXISTS idx_owner_name;")

def recreate_indexes_and_constraints(curs):
    print("Recreating foreign key and indexes...")
    curs.execute("ALTER TABLE pet ADD CONSTRAINT pet_id_owner_fkey FOREIGN KEY (id_owner) REFERENCES owner(id_owner);")
    curs.execute("CREATE INDEX idx_owner_name ON owner(name);")
    curs.execute("CREATE INDEX idx_pet_name ON pet(name);")
    curs.execute("CREATE INDEX idx_pet_owner_id ON pet(id_owner);")

def insert_owners(curs, conn):
    print("=== INSERTING INTO OWNER TABLE ===")
    t0 = time.time()
    for start in tqdm(range(0, N_OWNERS, BATCH_SIZE)):
        batch = [(start + i, random_name()) for i in range(BATCH_SIZE)]
        execute_batch(curs, "INSERT INTO owner (id_owner, name) VALUES (%s, %s);", batch)
        conn.commit()
    t1 = time.time()
    print(f"Inserted {N_OWNERS} owners in {t1 - t0:.2f}s ({N_OWNERS / (t1 - t0):.0f} rows/sec)")
    return t1 - t0

def generate_pet_csv():
    print("=== GENERATING CSV FILE FOR PET TABLE ===")
    t0 = time.time()
    with open(CSV_FILE, "w") as f:
        for i in tqdm(range(N_PETS)):
            f.write(f"{i},{random.randint(0, N_OWNERS - 1)},{random_name()}\n")
    t1 = time.time()
    print(f"File '{CSV_FILE}' created in {t1 - t0:.2f}s")
    return t1 - t0

def load_pets_with_copy(curs, conn):
    print("=== LOADING PET TABLE USING COPY ===")
    t0 = time.time()
    with open(CSV_FILE, "r") as f:
        curs.copy_from(f, "pet", sep=",", columns=("id_pet", "id_owner", "name"))
    conn.commit()
    t1 = time.time()
    print(f"Copied {N_PETS} pets in {t1 - t0:.2f}s ({N_PETS / (t1 - t0):.0f} rows/sec)")
    return t1 - t0

def main():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS,
        host=DB_HOST, port=DB_PORT
    )
    curs = conn.cursor()

    #Disable settings
    disable_safety_settings(curs)
    conn.commit()
    curs.execute("SELECT pg_reload_conf();")

    # Drop indexes + constraints
    drop_indexes_and_constraints(curs)
    conn.commit()

    # Truncate tables
    print("Truncating tables")
    curs.execute("TRUNCATE TABLE pet, owner RESTART IDENTITY CASCADE;")
    conn.commit()

    #  Insert owner data
    owner_time = insert_owners(curs, conn)

    # Generate pet CSV
    csv_time = generate_pet_csv()

    # Load pet data with COPY
    copy_time = load_pets_with_copy(curs, conn)

    # Recreate constraints + indexes
    recreate_indexes_and_constraints(curs)
    conn.commit()

    # Enable safety back
    enable_safety_settings(curs)
    conn.commit()
    curs.execute("SELECT pg_reload_conf();")

    curs.close()
    conn.close()

    total = owner_time + csv_time + copy_time
    print("\n=== DONE ===")
    print(f"Total rows: {N_OWNERS + N_PETS}")
    print(f"Total time: {total:.2f}s")
    print(f"Overall speed: {(N_OWNERS + N_PETS) / total:.0f} rows/sec")

if __name__ == "__main__":
    main()
