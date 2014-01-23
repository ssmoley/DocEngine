import psycopg2

conn = psycopg2.connect("dbname=postgres user=postgres")

cur = conn.cursor()

cur.execute("select * from dbo.main")

cur.fetchone()

#cur.execute("CREATE TABLE dbo.test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO dbo.test (num, data) VALUES (%s, %s)",(100, "abc'def"))

# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM dbo.test;")


#for i in cur:
print cur.fetchone()
print cur.fetchone()
print cur.fetchone()
print cur.fetchone()
print cur.fetchone()
print cur.fetchone()

#(1, 100, "abc'def")

# Make the changes to the database persistent
conn.commit()