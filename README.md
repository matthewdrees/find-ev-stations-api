# find-ev-stations-api
REST api for finding EV stations in the USA.

# Configuration

Running on Amazon Linux 2023.

    $ ssh -l ec2-user -o "IdentitiesOnly=yes" -o "PreferredAuthentications=publickey" -i .ssh/my_ec2_instance_key_pair.pe
m ec2-xx-xx-xx-xx.us-west-2.compute.amazonaws.com
    $ sudo dnf install python3-pip python3-devel nginx postgresql15 postgresql15-server libpq-devel
    $ pip3 install fastapi psycopg2 gunicorn

Instructions for setting up postgresql database here: <https://linux.how2shout.com/how-to-install-postgresql-15-amazon-linux-2023/>

    $ sudo postgresql-setup --initdb
    $ sudo systemctl start postgresql
    $ sudo systemctl enable postgresql

Find the postgres config file ...
    $ sudo -u postgres psql
    # SHOW hba_file;
    /var/lib/pgsql/data/pg_hba.conf

... and enable [trust authentication](https://www.postgresql.org/docs/current/auth-trust.html) for now.

    $ sudo vim /var/lib/pgsql/data/pg_hba.conf

    # "local" is for Unix domain socket connections only
    local   all             all                                     trust # changed from "peer"

    $ sudo systemctl restart postgresql

Get a [developer.nrel.gov key](https://developer.nrel.gov/signup/). Put it in config.json "nrel_key".

Fetch nrel data to a CSV file suitable for import to postgres.

    $  python3 get_stations_csv.py -v
    ...
    INFO:root:writing ev stations csv to '/tmp/stations.csv'

Create a table in the database and import the CSV file data.

    $ psql -U postgres
    # CREATE TABLE stations ... (from stationsdb.sql)
    # COPY stations FROM '/tmp/stations.csv';
    # exit

TODO: gunicorn service stuff and daemon reload

https://docs.gunicorn.org/en/stable/deploy.html
