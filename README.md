# READme für Makeathon @ Vitronic

## Wer das liest ist doof
lol stimmt

## ESP32

##PiCAM

## Database

For the database a postgresql database will be used.

### Setup
The database stores data in the folder, specified in the docker-compose.yaml in line XXX. The specified folder structure
needs to be created at first.After creating the folder. The container can be started.
To setup the postgreSQL database, run the given docker-compose.yaml with ```docker compose up -d```
If this does not work try with ```docker-compose up -d```. This will get postgresql database running.
The Docker Container will open the port 5432 foor connections.

### Connection and useful commands

To use the database via a terminal the following command can be used to connect to it:
- ```psql -h <Host IP> -p 5432 -U vitronic -d vitronicdb```

### vitronic 
for the usecase of vitronic, a table needs to be setup additionally. For this the setup.sql script can be used.
To create the infrastructure needed, run the vitronic_setup.sql via ```add command here```. To clean up the infrastructure,
run the vitronic_cleandb.sql via ```add command here``` 

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
