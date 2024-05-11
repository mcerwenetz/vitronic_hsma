# READme für Makeathon @ Vitronic

## Wer das liest ist doof

lol stimmt

## ESP32

## PiCAM

## Database

Als Datenbank wird eine PostgreSQL Datenbank verwendet.

### Setup

Über das docker-compose.yaml File kann die PostgreSQL DB auf dem PI gestarted werden. Dafür kann ```docker compose up -d``` verwendet werden. Die Daten werden auf dem Pi in einem eigenen Ordner abgelegt, dieser Ordner muss im docker-compose in Zeile 14 angegeben werden. Der erzeugte Container lässt Verbindungen auf Port 5432 zu.
Nachdem der Container erzeugt wurde, müssen zusätzlich die Tabellen für den Vitronic use case hinzugefügt werden. Die nötigen Schritt dafür sind im Kapitel [vitronic].

### Connection and useful commands

Über ein Terminal kann mmit folgendem Befehl eine Verbindung zur Datenbank aufgebaut werden:

- ```psql -h <Host IP> -p 5432 -U vitronic -d vitronicdb```

|cmd     |description              |
|:-------|:------------------------|
|\l      |show databases           |
|\c  (db)|connect to database      |
|\dt (db)|show tables of a database|
|\i (sql)|run specified sql file   |

### vitronic

Um die Tabellen in der vitronicdb zu erzeugen, kann das bereitgestellte sql Skript verwendet werden. Um das Skript auszuführen muss über das Terminal eine Verbindung zur DB bereitgestellt werden (siehe Kapitel davor). Nach erfolgreicher Verbindung zur Datenbank, kann das bereitgestellte Skript innerhalb der Datenbank ausgeführt werden: Dafür wird ```\i vitronic_setup.sql ``` verwendet. Um die erzeugte Tabelle wieder zu löschen, kann das vitronic_cleanupdb.sql Skript über  ```\i vitronic_cleandb.sql``` verwendet werden.

#### Table content

The following attributes are part of the table within the database and connected to each package:

|type    |Attribute           |Descritpion                                               |
|:-------|:-------------------|:---------------------------------------------------------|
|SERIAL  |id                  |PaketId , (aut-increment int)                             |
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
- MISSING
