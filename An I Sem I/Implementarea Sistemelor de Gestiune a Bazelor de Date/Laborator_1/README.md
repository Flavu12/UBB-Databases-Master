# Lab 1 — Bulk Insert Performance in PostgreSQL


## 1. Objective

- Create a database with two related tables (`owner` and `pet`) totaling ≥10M rows.  
- Achieve an insert rate ≥ 100,000 rows per second.  
- Design with **indexes**, **foreign keys**, and **performance tuning** for analytical workloads.  




## 2. PostgreSQL Installation (in WSL)

```bash
# Update the system
sudo apt update && sudo apt upgrade -y

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start PostgreSQL service
sudo service postgresql start

```
Verify installation:
```
sudo -u postgres psql
```

## 3. Create Database and Tables

```
CREATE DATABASE lab1_isgbd;
\c lab1_isgbd

CREATE TABLE owner (
  id_owner BIGINT PRIMARY KEY,
  name TEXT
);

CREATE TABLE pet (
  id_pet BIGINT PRIMARY KEY,
  id_owner BIGINT NOT NULL,
  name TEXT,
  FOREIGN KEY (id_owner) REFERENCES owner(id_owner)
);

```

## 4. Python Script — Bulk Insert Generator
Create a file called generator.py inside your WSL home directory or project folder.

1. Disables safety settings temporarily (fsync, synchronous_commit, full_page_writes)


2. Drops indexes and foreign keys before loading

3. Truncates existing data automatically

4. Inserts owners using batched INSERTs (50,000 rows at a time)

5. Generates a CSV for pets and loads it using COPY (faster than INSERT)

6. Recreates indexes and constraints after loading

7. Restores safety settings

```
pip install psycopg2-binary tqdm
python3 generator_v3.py
```
The script will automatically connect to PostgreSQL and insert 10 million rows (5M in each table).

## 5. Exemple Output
```
Disabling safety settings for bulk load...
Dropping foreign key and indexes...
Truncating tables...
=== INSERTING INTO OWNER TABLE ===
100%|█████████████████████████████████████████████████████████████████████████████████| 100/100 [02:03<00:00,  1.23s/it]
Inserted 5000000 owners in 123.32s (40546 rows/sec)
=== GENERATING CSV FILE FOR PET TABLE ===
100%|█████████████████████████████████████████████████████████████████████| 5000000/5000000 [00:15<00:00, 324241.86it/s]
File 'pet.csv' created in 15.42s
=== LOADING PET TABLE USING COPY ===
Copied 5000000 pets in 17.56s (284733 rows/sec)
Recreating foreign key and indexes...
Re-enabling safety settings...

=== DONE ===
Total rows: 10000000
Total time: 156.30s
Overall speed: 63980 rows/sec
```

Verify counts

```
lab1_isgbd=# SELECT COUNT(*) FROM owner;
  count
---------
 5000000
(1 row)

lab1_isgbd=# SELECT COUNT(*) FROM pet;
  count
---------
 5000000
(1 row)
```
## 6. Analytics workload


```

lab1_isgbd=# EXPLAIN ANALYZE
lab1_isgbd-# SELECT * FROM pet WHERE name LIKE 'f%';
                                            QUERY PLAN                                                  
----------------------------------------------------------------------------------------------------
 Gather  (cost=1000.00..78958.17 rows=151515 width=25) (actual time=0.407..233.062 rows=191465 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   ->  Parallel Seq Scan on pet  (cost=0.00..62806.67 rows=63131 width=25) (actual time=0.058..215.105 rows=63822 loops=3)
         Filter: (name ~~ 'f%'::text)
         Rows Removed by Filter: 1602845
 Planning Time: 0.058 ms
 Execution Time: 243.620 ms
(8 rows)


lab1_isgbd=# EXPLAIN ANALYZE
lab1_isgbd-# SELECT o.name AS owner_name, p.name AS pet_name
lab1_isgbd-# FROM owner o
N pet p ON o.id_ownlab1_isgbd-# JOIN pet p ON o.id_owner = p.id_owner
lab1_isgbd-# LIMIT 15;
                                            QUERY PLAN                                                        
------------------------------------------------------------------------------------------------------
  Limit  (cost=4.91..6.43 rows=15 width=18) (actual time=0.086..0.157 rows=15 loops=1)
   ->  Merge Join  (cost=4.91..506871.56 rows=5000000 width=18) (actual time=0.085..0.155 rows=15 loops=1)
         Merge Cond: (o.id_owner = p.id_owner)
         ->  Index Scan using owner_pkey on owner o  (cost=0.43..161699.43 rows=5000000 width=17) (actual time=0.045..0.047 rows=12 loops=1)
         ->  Index Scan using idx_pet_owner_id on pet p  (cost=0.43..270174.39 rows=5000000 width=17) (actual time=0.018..0.081 rows=15 loops=1)
 Planning Time: 1.125 ms
 Execution Time: 0.292 ms
(7 rows)
```
## 7. Notes on Performance
- Using batch inserts for owner gives a good balance between simplicity and performance
- Using COPY for pet allows bulk loading of millions of rows efficiently
- Using batch INSERT on a table with a foreign key can slow down performance due to constraint checks on each row.
- Indexes were created after bulk load to avoid slowing down insertions