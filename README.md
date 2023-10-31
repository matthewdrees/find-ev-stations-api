# find-ev-stations-api
REST api for finding EV stations in the USA.

# Configuration

Running on Amazon Linux 2023.

    $ sudo dnf install python3-pip python3-devel nginx postgresql15 postgresql15-server libpq-devel
    $ pip3 install fastapi psycopg2 gunicorn

Instructions for setting up postgresql database here: <https://linux.how2shout.com/how-to-install-postgresql-15-amazon-linux-2023/>

    sudo postgresql-setup --initdb
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
