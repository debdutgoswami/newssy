# Newsfeed

---

## Contributing

1. Check [CODE OF CONDUCT](https://github.com/debdutgoswami/newsfeed/blob/master/CODE_OF_CONDUCT.md) to know how to setup your `development` enviornment.

2. All PRs should be merged to `development` branch. So always change to `development` branch.

---

## Development

1. Clone the repository

2. Download `redis` for `email queue`

3. Create a `virtual environment` for python inside `app/api`

4. Change directory to `app/` and activate the `venv` and install all modules from `requirements.txt` using `pip`

5. Then run `redis server`.

6. Create a `start_api.sh` script which will export all the `environment variables` and will run the flask app and also `Celery`. To know how to run `Celery`, again refer to the [link](https://pratos.github.io/2017-01-12/celery-setup-on-windows/) provided in the previous step.


### Setting up PostgreSQL for development

1. Install postgresql

2. Start the service by typing `service postgresql start`

3. (optional) To connect to the database via CLI, type, `sudo -u <username> psql`. The default username is `postgres`

    To connect to database, type `\c <databasename>` in psql CLI. Here, the name is `newsfeed`.

    Type `\dt` to list the tables inside the database.

    Type `select * from <tablename>` to show the entire content of the database.

### Setting up Redis for development

1. Install redis server

2. Start the service by typing `service redis-server start`

3. (optional) Connect to redis via redis-cli, type `redis-cli` then type `ping` in the cli