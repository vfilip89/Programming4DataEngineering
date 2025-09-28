# A06 — SQL Libraries with Postgres & pgAdmin (Containerised)

This project demonstrates a **multi-container Docker Compose setup** with:
- **Postgres** (SQL database)
- **pgAdmin4** (web-based UI for database management)

It is part of my data engineering learning path and portfolio. It shows how to:
- Work with **SQL schemas, tables, joins, and queries**
- Use both **pgAdmin** and the **psql CLI** for database operations
- Configure and persist data with **Docker volumes**
- Perform **backups and restores** of Postgres and pgAdmin volumes

---

## 🚀 Project Structure

```
data-eng-sql-postgres-pgadmin/
├── compose.yaml                  # Docker Compose file (Postgres + pgAdmin)
├── backup.sql                    # SQL dump of database schema & data 
├── pgadmin-data-backup.tar.gz    # Backup archive of pgAdmin persistent volume
└── postgres-data-backup.tar.gz   # Backup archive of Postgres persistent volume
```

---

## 🐳 Running the Containers

Start the environment:

```bash
docker compose up -d
```

Check status:

```bash
docker compose ps
```

Output example:

```bash
[+] Running 30/30
 ✔ postgres Pulled                                                        38.3s
 ✔ pgadmin4 Pulled                                                        42.4s

[+] Running 5/5
 ✔ Network data-eng-sql-postgres-pgadmin_default       Created             0.1s
 ✔ Volume data-eng-sql-postgres-pgadmin_postgres-data  Created             0.0s
 ✔ Volume data-eng-sql-postgres-pgadmin_pgadmin-data   Created             0.0s
 ✔ Container postgres                                  Healthy            11.8s
 ✔ Container pgadmin4                                  Started            11.4s

```


### 🔑 Access the services

- **pgAdmin**: open [http://127.0.0.1:5050](http://127.0.0.1:5050) in your browser.  

👉 **First-time setup in pgAdmin**:  

1. Click **Add New Server**.  
2. Fill in the following:  
   - General → Name: `postgres`  
   - Connection → Host name/address: `postgres` (this matches the service name in `compose.yaml`)  
   - Port: `5432`  
   - Maintenance database: `postgres`  
   - Username: `postgres`  
   - Password: `postgres`  
3. Click **Save** → you should now see your Postgres server listed in the sidebar.  



- **psql CLI** (direct access via terminal):  

```bash
# Open a psql session inside the running postgres container
docker compose exec postgres psql -U postgres
```
---

## 🗂️ Detailed SQL-Tutorial Workflow

We use the psql CLI inside the Postgres container to practice SQL.  
Below is a step-by-step workflow with code, comments, and screenshots from pgAdmin for visualisation.

```sql
-- Create a new database called, e.g., 'mydb'
CREATE DATABASE mydb;
\c mydb
```
![alt text](images4READme/01-create-db.png)

✅ Output: We are now connected to database "mydb" as user "postgres".

```sql
-- Create a table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    date_of_birth DATE
);
```
🔎 Check available tables using CLI or pgAdmin 

```sql
\dt
```
![alt text](images4READme/02-check-tables.png)



```sql
-- Insert rows
mydb=# INSERT INTO users (first_name, last_name, email, date_of_birth) VALUES
('John', 'Doe', 'john.doe@example.com', '1990-01-01'),
('Jane', 'Smith', 'jane.smith@example.com', '1992-05-15'),
('Alice', 'Johnson', 'alice.johnson@example.com', '1985-10-20'),
('Bob', 'Williams', 'bob.williams@example.com', '1998-07-30'),
('Emily', 'Clark', 'emily.clark@example.com', '1987-02-14'),
('Michael', 'Robinson', 'michael.robinson@example.com', '1995-06-05'),
('Sarah', 'Lewis', 'sarah.lewis@example.com', '1989-03-25'),
('David', 'Walker', 'david.walker@example.com', '1992-11-12'),
('Sophia', 'Hall', 'sophia.hall@example.com', '1996-08-08'),
('James', 'Allen', 'james.allen@example.com', '1984-04-20'),
('Olivia', 'Young', 'olivia.young@example.com', '1993-12-30'),
('Chris', 'King', 'chris.king@example.com', '1990-09-15'),
('Grace', 'Wright', 'grace.wright@example.com', '1997-05-10'),
('William', 'Scott', 'william.scott@example.com', '1986-07-22');

-- Query data
SELECT * FROM users;
```
📊 Example query output:
![alt text](images4READme/03-query-users.png)

Let's proceed with updating data and 🔎 querying data

```sql
-- Get all unique email addresses
SELECT DISTINCT email FROM users;
```
![alt text](images4READme/04-distinct-emails.png)

```sql
-- Select all users with first_name = 'John'
SELECT * FROM users WHERE first_name = 'John';
```
![alt text](images4READme/05-users-john.png)

```sql
-- Update John's email address
UPDATE users SET email = 'new_email@gmail.com' WHERE first_name = 'John';
```
![alt text](images4READme/06-update-john.png)

```sql
-- Order users by ID
SELECT * FROM users ORDER BY id;
```
![alt text](images4READme/07-users-ordered.png)












---

## 💾 Backups & Restores

### Dump database to SQL file
```bash
docker compose exec postgres pg_dump -U postgres -d mydb > backup.sql
```

### Restore database from dump
```bash
docker compose exec postgres psql -U postgres -c "CREATE DATABASE mydb;"
docker compose exec -T postgres psql -U postgres -d mydb < backup.sql
```

### Backup persistent volumes
```bash
# Postgres data
docker run --rm \
  -v data-eng-sql-postgres-pgadmin_postgres-data:/volume \
  -v $(pwd):/backup \
  alpine \
  tar -czf /backup/postgres-data-backup.tar.gz -C /volume .

# pgAdmin data
docker run --rm \
  -v data-eng-sql-postgres-pgadmin_pgadmin-data:/volume \
  -v $(pwd):/backup \
  alpine \
  tar -czf /backup/pgadmin-data-backup.tar.gz -C /volume .
```

### Restore persistent volumes
```bash
docker run --rm \
  -v data-eng-sql-postgres-pgadmin_postgres-data:/volume \
  -v $(pwd):/backup \
  alpine \
  sh -c "cd /volume && tar -xzf /backup/postgres-data-backup.tar.gz"

docker run --rm \
  -v data-eng-sql-postgres-pgadmin_pgadmin-data:/volume \
  -v $(pwd):/backup \
  alpine \
  sh -c "cd /volume && tar -xzf /backup/pgadmin-data-backup.tar.gz"
```

---

## 📚 Learning Outcomes

- Learned to orchestrate **multi-container apps** with Docker Compose.
- Worked with **persistent volumes** to preserve database state.
- Practiced **SQL (DDL, DML, queries, joins, subqueries, unions)**.
- Used both **CLI (psql)** and **GUI (pgAdmin)** for DB management.
- Automated **backup & restore** processes for both Postgres and pgAdmin.

---

📌 This mini-project demonstrates practical **data engineering fundamentals**: containerisation, database persistence, SQL practice, and backup strategies.
