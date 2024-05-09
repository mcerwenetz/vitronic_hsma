# READme für Makeathon @ Vitronic

## Wer das liest ist doof
lol stimmt

## ESP32

## PiCAM

## Database

For the database a postgresql database will be used.

### Setup
The database stores data in the folder, specified in the docker-compose.yaml in line XXX. The specified folder structure
needs to be created at first.After creating the folder. The container can be started.
To setup the postgreSQL database, run the given docker-compose.yaml with ```docker compose up -d```
If this does not work try with ```docker-compose up -d```. This will get postgresql database running.
The Docker Container will open the port 5432 foor connections.
After successfully setting up the docker container go to the 'vitronic chapter' to setup the tables within the database.

### Connection and useful commands

To use the database via a terminal the following command can be used to connect to it:
- ```psql -h <Host IP> -p 5432 -U vitronic -d vitronicdb```

|cmd     |description              |
|:-------|:------------------------|
|\l      |show databases           |
|\c  <db>|connect to database      |
|\dt <db>|show tables of a database|
|\i <sql>|run specified sql file   |

### vitronic 

For the usecase of vitronic, a table with the package info needs to be added to the databse. For this the vitronic_setup.sql script can be used.
First of all, connect to the database via the connection command above. Pay attention, that you connect to the database within the folder, the *.sql files are located at. After successfully loggin in to the Postgre DB, connect to the vitronicdb Database with ```\c vitronicdb```. After connectoing to the DB the vitronic_setup.sql file can be run. The script can be run with ```\i vitronic_setup.sql ```. To delete the created table the vitronic_cleanupdb.sql script can be used with ```\i vitronic_cleandb.sql``` can be used.

#### Table content

The following attributes are part of the table within the database and connected to each package:

|type    |Attribute           |Descritpion                                               |
|:-------|:-------------------|:---------------------------------------------------------|
|????    |id                  |PaketId                                                   |
|int     |lastSeenAtGate      |At which gate was the package last seen                   |
|int     |length              |Length of package                                         |
|int     |hight               |Hight of package                                          |
|datetime|lastSeenAtTime      |timestamp, when the package past the gate                 |
|datetime|expectedAtNextGateAt|timestamp, when the package should arrive at the next gate|
|int     |status              |linuxlike status of the package                           |

#### Available package status

- OK
- DEFECTIVE
- CHINA
- Missing
