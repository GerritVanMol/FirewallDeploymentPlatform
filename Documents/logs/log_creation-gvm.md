# Bachelorproef LOGBOEK

### 1. Server firewall updaten (activeren en poorten openen)
- `sudo ufw allow ssh`
- `sudo ufw allow 80/tcp`
- `sudo ufw allow 8080/tcp`
- `sudo ufw status numbured` (controle open poorten)
        ![UFW Open poorten](https://i.imgur.com/U8JEAA3.png)

- `sudo ufw enable` (firewall activeren bij opstart)
        ![Controle firewall enabled](https://i.imgur.com/W7xBTvJ.png)

___
### 2. Opstellen virtuele omgeving
- python3 versie controleren:
    ![Python3 versie controle](https://i.imgur.com/ZdV00lZ.png)

- `sudo apt install python3-venv` (ondersteuning voor virtuele omgevingen)
- `python3 -m venv .venv-platform` (maken folder in virtuele omgeving)
- `. .venv-platform/bin/activate` (activeren => kan alleen in folder waar virtuele omgeving map staat)
        ![Controle activatie venv omgeving](https://i.imgur.com/cZ2LS65.png)


- `deactivate` (omgeving stoppen)
___

### 3. Installeren van Django in virtuele omgeving
 
- `pip3 install django`
- `python 3 -m django --verion` (controle succesvolle installatie)
    ![Django versie controle](https://i.imgur.com/RicYiYl.png)

    ~~`sudo apt install python3-django`~~    
___

### 4. Creeren van project structuur (in virtuele omgeving folder)
- `cd .venv-platform`
- `django-admin startproject siteplatform`
        ![Controle project in juiste (venv) folder](https://i.imgur.com/WHN0QU9.png)


- **Activeren Django site (test)**
    - `cd` naar project folder (`siteplatform`)
    - `ls` voor controle projet inhoud
    ![Controle project inhoud](https://i.imgur.com/yw6KfEF.png)

- **Foutmelding (geen migraties voor de databank)!**
    ![Error geen migraties](https://i.imgur.com/pfH8KNw.png)    
    **Resolutie:** `python3 manage.py migrate`


    - `python3 manage.py runserver 10.0.89.147:8080` (starten dev server)

- **Foutmelding (geen hosts toegelaten tot server)**
    ![Error host disallowed](https://i.imgur.com/6j0fPP8.png)
    **Resolutie:** voeg `'*'` toe aan `ALLOWED_HOSTS[]` in `~/siteplatform/settings.py`

    ![ALLOWED_HOSTS var in settings.py](https://i.imgur.com/ItHZ5N7.png)
     
     - `python3 manage.py runserver 10.0.89.147:8080` (starten dev server)
![Django default succes site](https://i.imgur.com/4BYTs25.png)


- **Installeren van extra packages (voor los koppelen van "env" omgeving variabelen)**
    - `pip3 install python-decouple`
    Package zal er voor zorgen dat paswoorden en secret keys niet worden mee vertaald naar de productie versie. Deze package zal er ook voor zorgen dat confidentiele data niet worden mee genomen daar een Git repository.


- **Copy maken van nodige packages**
    - `pip3 freeze > requirements.txt`
___
### 5. Python decouple package activeren
-  In `~/siteplatform/settings.py` wordt`from decouple import config` toegevoegd

- Bestand aan maken in zelfde folder als `manage.py` genaamd `.venv`:
- `touch .venv`, dit bestand bevat volgende variabelen:
    ```
    SECRET_KEY = django-**-app-**-secret-**-key-**hier
    DEBUG = True
    ALLOWED_HOSTS = 10.0.89.147

    #DB CONNECTION
    DB_ENGINE = django.db.backends.sqlite3
    DB_NAME = db.sqlite3
    DB_USER =
    DB_HOST =
    DB_PASSWD =
    DB_PORT =

    #Email settings
    EMAIL_HOST =
    EMAIL_PORT =

    #Time
    TIME_ZONE = UTC
    ```

Alle (vermelde) variabelen van in `.venv` worden vervangen met `variabeleNaam = config('varabeleNaam')` in settings.py. 
(Voorbeeld); 
![Voorbeeld; vervaning statische waarden settins.py](https://i.imgur.com/DLeZLZi.png)

Omdat `ALLOWED_HOSTS` een lijst type verwacht moet hier het type worden omgevormd, origineel wordt een string type terug gegeven. Dit resulteerd in `ALLOWED_HOSTS = config('ALLOWED_HOSTS' ,cast=Csv())`.
Omdat `.venv` niet wordt opgenomen in Git door mijn `.gitignore` bestand, blijven alle variabelen lokaal op de server staan en worden de waarder er van niet vrijgegeven.
De waarden in bovenstaande voorbeeld worden later aangepast aangezien er nog geen eigen databank is aangemaakt.

- Testen of applicatie nog werkt zo als het hoort; `python3 manage.py runserver 10.0.89.147:8080`

- **Foutmelding, "UndifinedValueError"!**
    ![Error decouple.UndifinedValueError](https://i.imgur.com/WU1BcB3.png)
**Resolutie:** 
Het bestand `.venv` had een verkeerde benaming en moest `.env` zijn.

Opnieuw testen van server (`python3 manage.py runserver 10.0.89.147:8080`):
![Django app back online](https://i.imgur.com/h2TyWzi.png)

### 6. Nieuwe "venv" omgeving

Omdat ik een foutje had gemaakt met mijn eerst virtuele omgeving en voor die map een `.` had gezet, bleef deze in hidden files staan. Waardoor ik deze ook op de Git moest forceren. Maar omdat deze er op werdt geforceerd werden alle andere files ook zichtbaar. Daarom heb ik de project folder hernoemt. 
Maar daarvoor moest ook de `venv` omgeving opnieuw worden gemaakt. Stappen die ik heb genomen;
- `sudo rm -rf venv` (verwijderen virtuele omgeving)
- `python3 -m venv my_platfrom` (nieuwe map maken)
- Alle bestanden van oude map (`.venv_platform`) naar nieuwe overmaken (`my_platform`)
- Omgeving opstarten `. myplatfrom/bin/activate`
- `pip3 install requirements.txt` (terug installeren van nodige packages)
___
### 7. Aanmaken deployment gebruiker

Gebruiker aan maken gebeurt best op root gebruiker account; `sudo su`.

Gebruiker zelf maken: `adduser deployment-user` daarna passwoord mee geven, alle andere velden zijn optioneel.
Voorbeeld gebruiker aanmaken;
    ![Add user in Ubuntu](https://i.imgur.com/NrJ0rqt.png)

Gebruiker toevoegen aan `sudo` groep: `usermod -aG sudo deployment-user`.

Controleren of gebruiker kan inloggen en of sudo commando's kunnen worden uitgevoerd; `sudo su deployment-user`.

**Succes**:
![New user, can perform required tasks](https://i.imgur.com/GJ93C9g.png)

#### 7.1 Gebruiker GitLab rechten geven
Omdat de nieuwe deployment-user nog geen rechten heeft tot de GitLab repository kan deze ook geen code gaan updaten. Daarom wordt er een met `ssh-keygen -t rsa` een key paar gemaakt om toe te voegen aan de GitLab instantie.

![Aan maken ssh keys](https://i.imgur.com/tIj5EN2.png)

Key output:
![PublicSSH_Key](https://i.imgur.com/NIPQYdt.png)

Key in GitLab toevoegen:
![Toevoegen public key op GitLab](https://i.imgur.com/6okxj07.png)

Nog beter zou zijn om een eigen GitLab instantie te draaien met daar een aparte deployment user. Op die manier kan deze user (in bedrijfswereld) niet worden ontslaan en kan er in elke situatie een nieuwe applicatie versie worden opgezet/ge pushed.

### 8. Opstellen PostgresSQL databank
(Bron is van [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04) voor opstellen PostgresSQL databank).

Installeren van extra packages voor databank:
`sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl`

Bij installatie van Postgres is een standaard gebruiker aangemaakt genaamd `postgres`.
Met deze gebruiker gaan we nu inloggen:`sudo -u postgres psql` 

![Postgres inlog voorbeeld](https://i.imgur.com/m5wlQFl.png)

- Maken van database
    - `CREATE DATABASE sitedb;`
    - `\l` (controle of DB is aangemaakt)
![Controle gemaakte DB](https://i.imgur.com/NgercV8.png)


- Maken van DB gebruiker
    - `CREATE USER siteuser WITH PASSWORD '1nfra&more';`
    - `\du` (controle aanmaak db gebruiker)
![Gebruiksers controle](https://i.imgur.com/xew3S0M.png)



### 9. Aanpassen parameters databank voor Django

Om Django goed te connecteren moeten er nog een aantal parameters worden gedefinieerd. Daarom voeren we volgende drie commando's uit;

1. `ALTER ROLE siteuser SET client_encoding TO 'utf8';`
2. `ALTER ROLE siteuser SET default_transaction_isolation TO 'read committed';`
3. `ALTER ROLE siteuser SET timezone TO 'UTC';` 
4. `GRANT ALL PRIVILEGES ON DATABASE sitedb TO siteuser;`
5. `\q` (quit => stop met configureren van database)

### 10. Update .env bestand

Omdat de databank nu is aangemaakt kunnen de omgevings variabelen worden aangepast naar de voorgaand gedefinieerde waarden de databank.
Het `.env` bestand ziet er als volgt uit:
```#Secret key purpose:     https://stackoverflow.com/questions/7382149/whats-the-purpose-of-django-setting-secret-key
    SECRET_KEY = mijn_key_****q2*h***^**vc***5_&!o3(w*
    DEBUG=True
    ALLOWED_HOSTS = 10.0.89.147,0.0.0.0

    #DB CONNECTION
    DB_ENGINE = django.db.backends.postgresql
    DB_NAME = sitedb
    DB_USER = siteuser
    DB_HOST = localhost
    DB_PASSWD = 1nfra&more
    DB_PORT = 5432

    #Email settings
    EMAIL_HOST =
    EMAIL_PORT =

    #Time
    TIME_ZONE = UTC
```

Om problemen met NGINX later te vermijden moet er nog een lijn code worden toegevoegd aan het `settings.py` bestand.
![Nginx statische pagina render](https://i.imgur.com/2meuzic.png)
Dit pad, "static_root" zorgt er voor dat NGINX statische pagina's zonder problemen kan terug vinden en weergeven (renderen) zoal het hoort.

### 11. Virtuele omgeving op deployment-user
De deployment user heeft nog geen virtuele omgeving, dus ook daar moet er een worden aangemaakt.

- `python3 -m venv venv` (-m = module, venv = module naam, 2de venv = virtuele omgeving naam)
- `. venv/bin/activate`

Om later de applicatie actief te laten, zonder deze in een terminal open te houden en te activeren zijn er nog een aantal packages nodig zoals "gunicorn" en eventueel "pillow".
- `pip3 install django python-decouple gunicorn psycopg2-binary pillow`
![Installeren van required packages](https://i.imgur.com/I2zLtzn.png)


### 12. Toepassen van database update (migreren)

Voor de Django applicatie terug kan in gebruik genomen worden moet de databank worden gemigreerd. 

- `python3 mangage.py migrate` (uitvoeren in map waar manage.py staat)

Voor ik de migratie succesvol was kreeg ik een aantal foutmeldingen:

1. Foutmelding:
In `settings.py` was de variabele `ENGINE` nog gelijk aan een statische waarde en deze statische waarde had eigenschappen van de standaard database `sqlite3`.
![Foutmelding verkeerde variabele voor DB engine](https://i.imgur.com/k8DU5N9.png)

**Resolutie:**
Statische waarde werd vervangen met `config('DB_ENGINE')` zo dat er wordt verwezen naar het `.env` bestand. Ook daar moest de DB engine nog worden aangepast naar `postgresql`.

2. Foutmelding:
3. Ubuntu firewall (UFW) liet poort 5432 nog niet toe.
![Poort niet toegelaten](https://i.imgur.com/gBmTrGq.png)
**Resolutie:**
Poort toelaten in UFW: `sudo ufw allow 5432/tcp`

3. Foutmelding: 

    ![No password supplied](https://i.imgur.com/pdmQTxU.png)
**Resolutie:**
In `settings.py`stond een variabele voor de databank nog op `PASSWD` en niet op `PASSWORD`.

**Succes migratie gelukt!**
![Migratie succesvol](https://i.imgur.com/WlXhewZ.png)



