#  Setting up PostgreSQL + InfluxDB + Telegraf

## 1️ PostgreSQL Setup
```bash
sudo -u postgres psql
CREATE USER telegraf WITH PASSWORD 'telegrafpass';
CREATE DATABASE postgresql;
GRANT ALL PRIVILEGES ON DATABASE postgresql TO telegraf;
```

## 2️ Create Table and Insert Data
```sql
CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name TEXT
);

INSERT INTO test_table (name) VALUES ('First');
INSERT INTO test_table (name) VALUES ('Second');
INSERT INTO test_table (name) VALUES ('Third');
```

## 3️ InfluxDB Setup
```bash
influx
CREATE DATABASE postgresql
```

## 4️ Telegraf Config Sample (place in /etc/telegraf/telegraf.conf)
```toml
[[inputs.postgresql_extensible]]
  address = "host=localhost user=telegraf password=telegrafpass dbname=postgresql sslmode=disable"

  [[inputs.postgresql_extensible.query]]
    sqlquery="SELECT count(*) as total_rows FROM test_table"
    version=0
    withdbname=false
    measurement="test_table_rows"
```

## 5️ Restart Telegraf
```bash
sudo systemctl restart telegraf
