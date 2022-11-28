# Steps for manual PostgreSQL orimary-secondary configuration

Guide used during configuration - [PostgreSQL Replication with Docker](https://medium.com/swlh/postgresql-replication-with-docker-c6a904becf77)

1. Get `primary-postgres.conf` file that will be used for future configuration:

```sh
docker run -i --rm postgres cat /usr/share/postgresql/postgresql.conf.sample > primary-postgres.conf
```

2. Change/uncomment the following lines

```sh
wal_level = replica
hot_standby = on
max_wal_senders = 10
max_replication_slots = 10
hot_standby_feedback = on
```

3. Create custom `primary-pg_hba.conf`:

```txt
# TYPE  DATABASE        USER            ADDRESS                 METHOD
# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     trust
host    replication     all             127.0.0.1/32            trust
host    replication     all             ::1/128                 trust
host    replication     replicator      0.0.0.0/0               trust
host all all all md5
```

4. Add configuration to primary container in `docker-compose-manual.yml`:

```yml
    volumes:
      - './postgres_configuration/primary-postgres.conf:/etc/postgresql/postgresql.conf'
      - './postgres_configuration/primary-pg_hba.conf:/etc/postgresql/pg_hba.conf'
```

4. Start primary database container:
```sh
docker-compose -f ./docker-compose-manual.yml up --detach --scale postgresql-primary=1 --scale postgresql-secondary=0
```

5. On the primary database to the following:

```sh
# Create the replicator user on master
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'my_replicator_password';

# Create the physical replication slot on master
SELECT * FROM pg_create_physical_replication_slot('replication_slot_slave1');

# To see that the physical replication slot has been created successfully, you could run this query:
SELECT * FROM pg_replication_slots;

```

6. Transfer backup from master database to slave:
```sh
# Get into container
docker exec -it <container_id> bash

# We need to get a backup from our master database and restore it for the slave.
pg_basebackup -D /tmp/postgresslave -S replication_slot_slave1 -X stream -P -U replicator -Fp -R

# On host machine execute the following:
docker cp <container_id>:/tmp/postgresslave/ ./data-secondary
```

7. Update some values from `postgresql.auto.conf` file inside the `data-secondary` directory with connection information and restore command:
```
primary_conninfo = 'host=127.0.0.1 port=5432 user=replicator password=my_replicator_password'
restore_command = 'cp /var/lib/postgresql/data/pg_wal/%f "%p"'
```

8. Run both master and slave
```sh
docker-compose -f docker-compose-manual.yml up --detach
```