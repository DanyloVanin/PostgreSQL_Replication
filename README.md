# PostgreSQL_Replication


## Infrastructure

### Simple configuration

Here we are using docker-compose file provided by Bitnami. Their Docker images already contain all configuration needed to start master-slave cluster.

[Bitnami postgresql repository](https://github.com/bitnami/containers/tree/main/bitnami/postgresql)

To run you can use:
```sh
docker-compose -f bitnami/docker-compose-replication.yml up --detach --scale postgresql-master=1 --scale postgresql-slave=1
```

## Manual configuration

Process described in [ManualConfiguration.md](./manual/ManualConfiguration.md)

## Sample python application
Python application is provided that creates reader and writer processes. Reader reads from specified database. Writer tries to write to specified database.

To use application:
```sh
cd python_example
pip3 install -r requirements.txt
python3 writer.py

# In another window 
python3 reader.py

```
## Problems thaht encountered and their solutions

First problem was with mounting local windows folder into postgres container to store data. It didn't work and is likely not supported. Had to move to volumes instead. 

There were also some problems with configuring `pg_hba.conf`, howerever, it turned out that the reason for the problem was that I was working with wrong configuration directory. After changing volume path the problem dissappered.


### Additional resources

- [Compose file version 3 reference](https://docs.docker.com/compose/compose-file/compose-file-v3/)
- [Bitnami postgresql repository](https://github.com/bitnami/containers/tree/main/bitnami/postgresql)
- [PostgreSQL Replication with Docker](https://medium.com/swlh/postgresql-replication-with-docker-c6a904becf77)