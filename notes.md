## Cheatsheet

```bash
conda env export | grep -v "^prefix: " > aerodev.yml
```

```bash
conda env create -f aerodev.yml
```

```bash
pip install typer
pip install -U black
pip install gpiozero pigpio

```

## chrontab
```bash
sudo crontab -e
```

```bash
@reboot nohup /home/pi/.conda/envs/aero/bin/python /home/pi/dev/aeropi/main.py &
@reboot /home/pi/redis-6.0.6/src/redis-server --daemonize yes
@reboot sudo service postgresql start
@reboot source activate aerodev
```


## tof

https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/python-circuitpython

```bash
pip install adafruit-circuitpython-vl53l0x
pip install adafruit-circuitpython-tca9548a
```

### GPIO
# https://www.raspberrypi.org/documentation/usage/gpio/
```bash
pinout
```

### ssh
```bash
ssh-keygen -p
```

### scan all ic devices

scan ic devices
```bash
# allow i2c: sudo raspi-config
i2cdetect -y 1
```


## postgres
```bash
sudo apt install postgresql libpq-dev postgresql-client
postgresql-client-common -y
```

setup user
```bash
createuser pi -P --interactive
```

crate db name same as user for easy login
```bash
CREATE DATABASE pi;
```

OR
```bash
psql --dbname=test
```

```bash
sudo su postgres
```

create table
```bash
create database <name>
```

start
```bash
sudo service postgresql start
```

grab db
`\connect` `\c` <name>
```bash
\c test
```

list tables
```bash
\dt
```

view size of table
```bash
select pg_size_pretty(pg_relation_size('users'));
```

drop table
```bash
DROP TABLE
```
quit
```
\q
```

## SQA
```bash
conda install -c anaconda sqlalchemy
pip install psycopg2
pip install sqlalchemy-utils
```


## redis

install [here](https://amalgjose.com/2020/08/11/how-to-install-redis-in-raspberry-pi/)
```bash
wget http://download.redis.io/releases/redis-6.0.6.tar.gz
tar xzf redis-6.0.6.tar.gz
cd redis-6.0.6
make
make test
```

queue len from cmd
```bash
redis-cli -h localhost -p 6379 -n 5 llen a
```

start
```
/home/pi/redis-6.0.6/src/redis-server --daemonize yes
```

check
```bash
ps aux | grep redis-server
```

kill
```bash
kill -9 $PID
```

## celery
```bash
celery -A cluster worker -l info -Q "collect" -n "main"
celery -A cluster worker -l info -Q "q_demux_run" -n "demux_run" -c 1
celery -A cluster worker -l info -Q "q_demux_log" -n "demux_log" -c 1
celery -A cluster worker -l info -Q "q_dists_run" -n "dists_run" -c 1
celery -A cluster worker -l info -Q "q_dists_log" -n "dists_log" -c 1
```
### Readbeat
```bash
pip install celery-redbeat
```

# TODO: https://docs.celeryproject.org/en/stable/userguide/daemonizing.html

```bash
pip install -U "celery[redis]"
```