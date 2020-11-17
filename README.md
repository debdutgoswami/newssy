# Newssy

An all-in-one news portal where anyone can look through news from various sources and even subscribe to newsletters to receive daily headlines via email.

---

## Contributing

1. All PRs should be merged to `development` branch. So always change to `development` branch.

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

Deployment (Google Cloud Platform)
======

### Setting CloudSQL

We will be using a postgresql. Follow this [documentation](https://cloud.google.com/sql/docs/postgres/connect-external-app#sqlalchemy-unix).

1. Create a service account key (JSON)

2. Download `cloud_sql_proxy` and make it executable using `chmod +x cloud_sql_proxy`

3. Create a user in the database and add an appropiate password

4. Create a database named `newsfeed`

5. Database URI should be of the following format <pre>postgresql+psycopg2://{username}:{password}@/?host=/cloudsql/{connection_name}</pre>

6. Run the proxy first. Type the following to run it. 
    <pre>./cloud_sql_proxy -dir=/cloudsql -instances={connection_name} \
                -credential_file={service_account_key} &</pre>

7. Now, create the tables. To create the tables, simply export the environment variables and then type the following in your terminal. <pre>python manage.py create_db</pre>
