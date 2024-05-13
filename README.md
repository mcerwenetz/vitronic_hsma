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

Um die Tabellen in der vitronicdb zu erzeugen, kann das bereitgestellte sql Skript verwendet werden. Um das Skript auszuführen muss über das Terminal eine Verbindung zur DB bereitgestellt werden (siehe Kapitel davor). Nach erfolgreicher Verbindung zur Datenbank, kann das bereitgestellte Skript innerhalb der Datenbank ausgeführt werden: Dafür wird ```\i vitronic_setup.sql``` verwendet. Um die erzeugte Tabelle wieder zu löschen, kann das vitronic_cleanupdb.sql Skript über  ```\i vitronic_cleandb.sql``` verwendet werden.

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

#### Python Scripts for interacting with the db

Im ./src/database/python Ordner sind 3 Python Skripte hinterlegt zur Interaktion mit der Datenbank. Das createData.py Skript modelliert klassische DB Interaktion. Das checkexpiry.py Skript überprüft regelmäßig anhand eines zeitstempels, ob Pakete fehlen. Beide Skripte nutzen im Hintergrund das sql_functiony.py Skript, das im Hintergrund die CRUD Operationen gegen die Datenbank ausführt.
Für die Skripte müssen eine zusätzliches ```lost.log``` Datei, sowie eine ```.env``` Datei erstellt werden. Im .env File müssen folgende Werte spezifiziert werden:

- DATABASE_HOST=[hostIP]
- DATABASE_PORT=[port]
- DATABASE_USER=[username]
- DATABASE_PASSWORD=[password]
- DATABASE=[databasename]

##### createData.py

Mit diesem Skript können beispielhaft Einträge der Datenbank hinzugefügt werden, die Einträge gelesen und veränder bzw. gelöscht werden. Für das Skript sind folgende Pytohn Bibliotheken zu installieren:

- ```pip install psycopg2-binary```
- ```pip install python-dotenv```

Nach Programmstart kann mit folgenden Kommandos auf die Anwendung zugegriffen werden:

|Kommando   |Erläuterung                          |
|----------:|:------------------------------------|
|q          |Anwendung beenden                    |
|add        |Eintrag der DB hinzufügen            |
|get        |Auflisten aller vorhandenen Einträge |
|clear      |Datenbankeinträge löschen            |
|update (id)|Paket mit id an neuem Gate angekommen|

Das Skript kann mit ```pytohn3 createData.py``` gestartet werden.

##### checkexpiry.py

Das Skript liest alle Einträge aus der DB aus und fügt Einträgen, die beim Zeitstempel Attribut [expectedNext] einen bereits verstrichenen Zeitpunkt hinterlegt haben das Status Bit LOST hinzu. Zusätzlich wird in einem Log File das fehlen des Paketes vermerkt. Das Programm kann mit einem Kommandozeilenargument gestarted werden. zum Programmstart kann eine Minutenanzahl hinugefügt werden. Das Programm läuft anschließend für die angegebene Anzahl an Minuten. Wird nichts angegeben läuft das Programm für 5 Minuten.

- Das Skript wird mit ```python3 checkexpiry.py <mins>``` gestartet.
