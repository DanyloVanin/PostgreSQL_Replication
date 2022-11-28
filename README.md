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

### Additional resources

- [Compose file version 3 reference](https://docs.docker.com/compose/compose-file/compose-file-v3/)
- [Bitnami postgresql repository](https://github.com/bitnami/containers/tree/main/bitnami/postgresql)
- [PostgreSQL Replication with Docker](https://medium.com/swlh/postgresql-replication-with-docker-c6a904becf77)