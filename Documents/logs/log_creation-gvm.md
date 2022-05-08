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


---


### 12. Maken van super user voor Django admin paneel

- `python3 manage.py createsuperuser`
![Maken van superuser](https://i.imgur.com/MHieCVB.png)

Statische waarden van applicatie opslaan:
- `python3 manage.py collectstatic`
![Opslaan statische files](https://i.imgur.com/FlD8H4g.png)

Testen applicatie met nieuwe databank configuratie:
![startup server](https://i.imgur.com/DnOTAAo.png)


Admin paneel:
![Applicatie admin paneel](https://i.imgur.com/eF3smLQ.png)

Inloggen als user `gerrit` met zelfde student WW:
![Logging in](https://i.imgur.com/cTCitBQ.png)

Admin paneel:
![Admin paneel (logged in)](https://i.imgur.com/sCq7B1s.png)

___
### 13. Gunicorn services
De web applicatie wordt op dit moment enkel gehost wanneer `python3 manage.py runserver 0.0.0.0:8080` in de terminal is uitgevoerd. Eenmaal deze terminal gesloten wordt, is de applicatie ook niet niet meer beschikbaar. Om dit te voorkomen en de applicatie ten alle tijden draaiende te houden zal er worden gerbuik gemaakt van Gunicorn.
- `gunicorn --bind 0.0.0.0:8080 siteplatform.wsgi` (bind gunicorn aan de web applicatie)
![](https://i.imgur.com/HkD90Nx.png)

Bovenstaand commando activeert de applicatie op de zelfde manier wanneer men de applicatie zou starten met Django maar dan met Gunicorn.
Om de applicatie draaiende te houden met Gunicorn moet er eerst de Gunicorn socket worden geconfigureerd.

- `sudo vim /etc/systemd/system/gunicorn.socket`

In dit bestand komt het volgende:
```
    [Unit]
    Description=gunicorn socket

    [Socket]
    ListenStream=/run/gunicorn.sock

    [Install]
    WantedBy=sockets.target
```
Met `sudo vim /etc/systemd/system/gunicorn.service` wordt een service bestand gemaakt.

In `gunicorn.service` komt het volgende:
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=deployment-user
Group=www-data
WorkingDirectory=/home/deployment-user/automationplatform/my_platform/siteplatform
ExecStart=/home/deployment-user/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          siteplatform.wsgi:application

[Install]
WantedBy=multi-user.target
```
Nu de socket is geconfigureerd kan de Gunicorn service worden gestart.
- `sudo systemctl start gunicorn.socket` (start service)
- `sudo systemctl enable gunicorn.socket` (activeer wanneer server opstart)
![](https://i.imgur.com/nBzFN2S.png)

**Wanneer enige aanpassingen worden gemaakt in het `gunicorn.service` bestand moet met de `daemon` en `gunicorn` reloaden.**
- `sudo sytemctl daemon-reload`
- `sudo systemctl restart gunicorn`



- `sudo systemctl status gunicorn` (controle service actief)
![](https://i.imgur.com/Xf5JmSf.png)


### 14. Nginx configuratie

Omdat Gunicorn de web applicatie wel actief houd maar niet door verwijst naar en poort waar men naar kan surfen zal er gebruik gemaakt worden van Nginx.

Voor Nginx kan worden geconfigureerd moet in het `.env` bestand van de Django applicatie de `DEBUG` variabele op `False` gezet worden.

Nu de DEBUG variable op false staat moet het project worden gelinked in de Nginx configuratie:

- `sudo vim /etc/nginx/sites-available/siteplatform`
In siteplatform:
```
server {
    listen 80;
    server_name 10.0.89.147;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/deployment-user/automationplatform/my_platform/siteplatform;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
Dit zorgt er voor dat Django zelf niet meer zal proberen om een web interface weer te geven, maar wordt deze taak door gegeven aan Nginx.
Als er straks een verzoek (reqeust) wordt gestuurd naar de app server, zal op poort `80` de applicatie beschikbaar zijn.
Voor dit kan moet deze 'site' enabled zijn:
- ` sudo ln -s /etc/nginx/sites-available/siteplatform /etc/nginx/sites-enabled`

Controleren of geen Nginx syntax fouten zijn gemaakt:
![](https://i.imgur.com/A54rHKZ.png)

Nu de configuratie is aangepast voor Nginx moeten de aanpassingen nog worden doorgevoerd door de service opnieuw op te starten.
- `sudo systemctl restart nginx`

Als men nu naar het IP suft van de server kan men de applicatie actief zien, zonder dat er bij de URL een poort nummer moet worden mee gegeven. Dat is omdat poort 80 werdt gedefinieerd als standaard in de Nginx configuratie.
![Web applicatie actief via Nginx](https://i.imgur.com/WIEP8MD.png)

**Wanneer aanpassingen gebeuren in de project (Django) bestanden moeten een aantal services opnieuw worden opgestart.** Dit moet voor men de applicatie kan gaan bekijken met deze aanpassingen en indien er niet wordt gewerkt met CI/CD.
1. `sudo systemctl restart nginx`
2. `sudo systemctl restart gunicorn`

___
## Jenkins server deploy/install
Jenkins minimum serverhardware requirements:
![Jenkins minimum requirements](https://i.imgur.com/RUaMuXJ.png)

In ESXI word een virtuele machine geconfigureerd/opgestart met de nodige resources:
![jenkins-srv resources](https://i.imgur.com/Dv8addJ.png)

Jenkins heeft Java nodig om te werken, daarom controleren of JDK al is geinstalleerd;
- `java --version`

(Java is nog niet geinstalleerd):
![](https://i.imgur.com/pNndeLc.png)

Installeren van JDK;
- `sudo apt install openjdk-8-jdk`
- `java -version` (controle succesvole installatie)
![](https://i.imgur.com/UV95iZA.png)

Installeren Jenkins Long Term Release:
![](https://i.imgur.com/7EnjhOY.png)

```
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

Succesvole Jenkins installatie:
![](https://i.imgur.com/XAZBmAS.png)

Om zeker te zijn kan er naar het server IP-adres (10.0.89.148) worden gegaan om te kijken of Jenkins actief is.
Jenkins wordt geserveerd op poort 8080, om deze pagina te bereiken moet de Ubuntu firewall (UFW) deze eerst toelaten:
- `sudo ufw allow 8080/tcp` (poort voor Jenkins)
- `sudo ufw allow ssh` (Mezelf niet buitensluiten voor toegang tot de server)
- `sudo ufw enable` (firewall updaten/opstarten wanner server opstart)

![Jenkins actief](https://i.imgur.com/nZxbuLa.png)

Om toegant te krijgen to de Jenkins omgeving moet het initeel paswoord worden ingegeven.
- `sudo cat /var/lib/jenkins/secrets/initialAdminPassword` (paswoord ophalen in terminal)
**Paswoord ingeven op webinterface:**
![](https://i.imgur.com/LcNlXdU.png)
**Installeren van gesuggereerde plugins:**
![](https://i.imgur.com/BVbm0WW.png)
![](https://i.imgur.com/dhRxfaq.png)

**Maken van nieuwe admin gebruiker:**
![](https://i.imgur.com/3HE83WC.png)

**Configureren van IP/URL waarop Jenkins zal actief zijn:**
![](https://i.imgur.com/Mp7gX8v.png)
![](https://i.imgur.com/3HpNzsY.png)



### Jenkins plugins

Nu Jenkins is geinstalleerd moeten er een aantal plugins worden geinstalleerd zo dat de web applicatie kan worden geupdate wanneer enige aanpassingen worden gepushed naar GitLab.
De nodige plugins daar voor zijn:
1. Git
2. GitLab

Op de Jenkins server in de plugin manager kan er worden gecontroleerd of deze plugins al dan niet zijn geinstallerd.

**Git plugin is al geinstalleerd:**
![](https://i.imgur.com/vwy9UxE.png)


**GitLab plugin is nog niet geinstalleerd:**
![](https://i.imgur.com/TuTJgO6.png)


**GitLab plugin installeren:**
![](https://i.imgur.com/J2Yrb5U.png)


### Jenkins access token

![](https://i.imgur.com/1nOCZlK.png)

**GitLab access token:**
![](https://i.imgur.com/YKcZw6T.png)

Omdat de access token maar éénmaal wordt weergegeven is deze opgeslagen op de Jenkins server:
![](https://i.imgur.com/g4V2FH5.png)

Nu de access token is aangemaakt kan deze worden toegevoegd op de Jenkins interface.

![](https://i.imgur.com/KAMPveN.png)

![](https://i.imgur.com/dOT4yTM.png)

Testen connectie:
![](https://i.imgur.com/r7qSXvh.png)

### Jenkins pipline configuratie

In een`jenkinsfile` wordt de pipline en zijn stages gedefinieerd. Deze file moet worden gemaakt in de folder structuur van de Django applicatie.

![](https://i.imgur.com/A3bxogL.png)

In dit (`jenkinsfile`) bestand komt het volgende:
```
pipeline {
    agent any 
    stages {
        stage('Build') { 
            steps {
                sh "echo 'building application'"
            }
        }
        stage('Test') { 
            steps {
                echo "testing"
            }
        }
        stage('Deploy') { 
            steps {
                sh  "echo deploying"
            }
        }
    }
}
```
De gedefineerde stages zijn zeer premitief, maar wordt later aangevuld.

**Configureren van pipline**

Maken van nieuw item:
![](https://i.imgur.com/53N4zFz.png)

Benoemen en aanmaken van nieuw item (pipline):
![](https://i.imgur.com/ZvBLxRv.png)

Pipline beschrijving geven en selecteren op welke manier verbinding wordt gemaakt (via api access token).

![](https://i.imgur.com/ZAEid2u.png)

Selecteren dat pipline script van een SCM (Git Source Management) komt. De error in onderstaande afbeelding is omdat GitLab nog geen SSH key heeft gedefinieerd van de Jenkins server.

![](https://i.imgur.com/JmwkqYN.png)

Repository van `*/master` vervangen naar `*/main`, script pad controleren en pipline opslaan.
![](https://i.imgur.com/BopH2r2.png)



**Resolutie pipline error (SSH key toevoegen in GitLab):**
Key pair aanmaken op de Jenkins-srv;
![](https://i.imgur.com/pLIvLWJ.png)

- `cd .ssh`
- `cat id_rsa.pub`
- Copy paste in GitLab ssh keys:
![](https://i.imgur.com/R9hmP5v.png)


De error blijft persisteren, mogelijks dat de Jenkins interface achterliggend de repository niet opnieuw gaat valideren. Daarom wordt de repo handmatig op de server gezet.

![](https://i.imgur.com/9lRoAtQ.png)
- `git ls-remote -h --git@gitlab.com:ikdoeict/gerrit.vanmol/automationplatform.git HEAD`
Voorgaand commando werd mee gegeven op de Jenkins interface
![](https://i.imgur.com/nJf96sY.png)



### 12. Maken van super user voor Django admin paneel

- `python3 manage.py createsuperuser`
![Maken van superuser](https://i.imgur.com/MHieCVB.png)

Statische waarden van applicatie opslaan:
- `python3 manage.py collectstatic`
![Opslaan statische files](https://i.imgur.com/FlD8H4g.png)

Testen applicatie met nieuwe databank configuratie:
![startup server](https://i.imgur.com/DnOTAAo.png)


Admin paneel:
![Applicatie admin paneel](https://i.imgur.com/eF3smLQ.png)

Inloggen als user `gerrit` met zelfde student WW:
![Logging in](https://i.imgur.com/cTCitBQ.png)

Admin paneel:
![Admin paneel (logged in)](https://i.imgur.com/sCq7B1s.png)

___
### 13. Gunicorn services
De web applicatie wordt op dit moment enkel gehost wanneer `python3 manage.py runserver 0.0.0.0:8080` in de terminal is uitgevoerd. Eenmaal deze terminal gesloten wordt, is de applicatie ook niet niet meer beschikbaar. Om dit te voorkomen en de applicatie ten alle tijden draaiende te houden zal er worden gerbuik gemaakt van Gunicorn.
- `gunicorn --bind 0.0.0.0:8080 siteplatform.wsgi` (bind gunicorn aan de web applicatie)
![](https://i.imgur.com/HkD90Nx.png)

Bovenstaand commando activeert de applicatie op de zelfde manier wanneer men de applicatie zou starten met Django maar dan met Gunicorn.
Om de applicatie draaiende te houden met Gunicorn moet er eerst de Gunicorn socket worden geconfigureerd.

- `sudo vim /etc/systemd/system/gunicorn.socket`

In dit bestand komt het volgende:
```
    [Unit]
    Description=gunicorn socket

    [Socket]
    ListenStream=/run/gunicorn.sock

    [Install]
    WantedBy=sockets.target
```
Met `sudo vim /etc/systemd/system/gunicorn.service` wordt een service bestand gemaakt.

In `gunicorn.service` komt het volgende:
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=deployment-user
Group=www-data
WorkingDirectory=/home/deployment-user/automationplatform/my_platform/siteplatform
ExecStart=/home/deployment-user/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          siteplatform.wsgi:application

[Install]
WantedBy=multi-user.target
```
Nu de socket is geconfigureerd kan de Gunicorn service worden gestart.
- `sudo systemctl start gunicorn.socket` (start service)
- `sudo systemctl enable gunicorn.socket` (activeer wanneer server opstart)
![](https://i.imgur.com/nBzFN2S.png)

**Wanneer enige aanpassingen worden gemaakt in het `gunicorn.service` bestand moet met de `daemon` en `gunicorn` reloaden.**
- `sudo sytemctl daemon-reload`
- `sudo systemctl restart gunicorn`



- `sudo systemctl status gunicorn` (controle service actief)
![](https://i.imgur.com/Xf5JmSf.png)


### 14. Nginx configuratie

Omdat Gunicorn de web applicatie wel actief houd maar niet door verwijst naar en poort waar men naar kan surfen zal er gebruik gemaakt worden van Nginx.

Voor Nginx kan worden geconfigureerd moet in het `.env` bestand van de Django applicatie de `DEBUG` variabele op `False` gezet worden.

Nu de DEBUG variable op false staat moet het project worden gelinked in de Nginx configuratie:

- `sudo vim /etc/nginx/sites-available/siteplatform`
In siteplatform:
```
server {
    listen 80;
    server_name 10.0.89.147;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/deployment-user/automationplatform/my_platform/siteplatform;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
Dit zorgt er voor dat Django zelf niet meer zal proberen om een web interface weer te geven, maar wordt deze taak door gegeven aan Nginx.
Als er straks een verzoek (reqeust) wordt gestuurd naar de app server, zal op poort `80` de applicatie beschikbaar zijn.
Voor dit kan moet deze 'site' enabled zijn:
- ` sudo ln -s /etc/nginx/sites-available/siteplatform /etc/nginx/sites-enabled`

Controleren of geen Nginx syntax fouten zijn gemaakt:
![](https://i.imgur.com/A54rHKZ.png)

Nu de configuratie is aangepast voor Nginx moeten de aanpassingen nog worden doorgevoerd door de service opnieuw op te starten.
- `sudo systemctl restart nginx`

Als men nu naar het IP suft van de server kan men de applicatie actief zien, zonder dat er bij de URL een poort nummer moet worden mee gegeven. Dat is omdat poort 80 werdt gedefinieerd als standaard in de Nginx configuratie.
![Web applicatie actief via Nginx](https://i.imgur.com/WIEP8MD.png)

**Wanneer aanpassingen gebeuren in de project (Django) bestanden moeten een aantal services opnieuw worden opgestart.** Dit moet voor men de applicatie kan gaan bekijken met deze aanpassingen en indien er niet wordt gewerkt met CI/CD.
1. `sudo systemctl restart nginx`
2. `sudo systemctl restart gunicorn`

___
## Jenkins server deploy/install
Jenkins minimum serverhardware requirements:
![Jenkins minimum requirements](https://i.imgur.com/RUaMuXJ.png)

In ESXI word een virtuele machine geconfigureerd/opgestart met de nodige resources:
![jenkins-srv resources](https://i.imgur.com/Dv8addJ.png)

Jenkins heeft Java nodig om te werken, daarom controleren of JDK al is geinstalleerd;
- `java --version`

(Java is nog niet geinstalleerd):
![](https://i.imgur.com/pNndeLc.png)

Installeren van JDK;
- `sudo apt install openjdk-8-jdk`
- `java -version` (controle succesvole installatie)
![](https://i.imgur.com/UV95iZA.png)

Installeren Jenkins Long Term Release:
![](https://i.imgur.com/7EnjhOY.png)

```
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

Succesvole Jenkins installatie:
![](https://i.imgur.com/XAZBmAS.png)

Om zeker te zijn kan er naar het server IP-adres (10.0.89.148) worden gegaan om te kijken of Jenkins actief is.
Jenkins wordt geserveerd op poort 8080, om deze pagina te bereiken moet de Ubuntu firewall (UFW) deze eerst toelaten:
- `sudo ufw allow 8080/tcp` (poort voor Jenkins)
- `sudo ufw allow ssh` (Mezelf niet buitensluiten voor toegang tot de server)
- `sudo ufw enable` (firewall updaten/opstarten wanner server opstart)

![Jenkins actief](https://i.imgur.com/nZxbuLa.png)

Om toegant te krijgen to de Jenkins omgeving moet het initeel paswoord worden ingegeven.
- `sudo cat /var/lib/jenkins/secrets/initialAdminPassword` (paswoord ophalen in terminal)
**Paswoord ingeven op webinterface:**
![](https://i.imgur.com/LcNlXdU.png)
**Installeren van gesuggereerde plugins:**
![](https://i.imgur.com/BVbm0WW.png)
![](https://i.imgur.com/dhRxfaq.png)

**Maken van nieuwe admin gebruiker:**
![](https://i.imgur.com/3HE83WC.png)

**Configureren van IP/URL waarop Jenkins zal actief zijn:**
![](https://i.imgur.com/Mp7gX8v.png)
![](https://i.imgur.com/3HpNzsY.png)



### Jenkins plugins

Nu Jenkins is geinstalleerd moeten er een aantal plugins worden geinstalleerd zo dat de web applicatie kan worden geupdate wanneer enige aanpassingen worden gepushed naar GitLab.
De nodige plugins daar voor zijn:
1. Git
2. GitLab

Op de Jenkins server in de plugin manager kan er worden gecontroleerd of deze plugins al dan niet zijn geinstallerd.

**Git plugin is al geinstalleerd:**
![](https://i.imgur.com/vwy9UxE.png)


**GitLab plugin is nog niet geinstalleerd:**
![](https://i.imgur.com/TuTJgO6.png)


**GitLab plugin installeren:**
![](https://i.imgur.com/J2Yrb5U.png)


### Jenkins access token

![](https://i.imgur.com/1nOCZlK.png)

**GitLab access token:**
![](https://i.imgur.com/YKcZw6T.png)

Omdat de access token maar éénmaal wordt weergegeven is deze opgeslagen op de Jenkins server:
![](https://i.imgur.com/g4V2FH5.png)

Nu de access token is aangemaakt kan deze worden toegevoegd op de Jenkins interface.

![](https://i.imgur.com/KAMPveN.png)

![](https://i.imgur.com/dOT4yTM.png)

Testen connectie:
![](https://i.imgur.com/r7qSXvh.png)

### Jenkins pipline configuratie

In een`jenkinsfile` wordt de pipline en zijn stages gedefinieerd. Deze file moet worden gemaakt in de folder structuur van de Django applicatie.

![](https://i.imgur.com/A3bxogL.png)

In dit (`jenkinsfile`) bestand komt het volgende:
```
pipeline {
    agent any 
    stages {
        stage('Build') { 
            steps {
                sh "echo 'building application'"
            }
        }
        stage('Test') { 
            steps {
                echo "testing"
            }
        }
        stage('Deploy') { 
            steps {
                sh  "echo deploying"
            }
        }
    }
}
```
De gedefineerde stages zijn zeer premitief, maar wordt later aangevuld.

**Configureren van pipline**

Maken van nieuw item:
![](https://i.imgur.com/53N4zFz.png)

Benoemen en aanmaken van nieuw item (pipline):
![](https://i.imgur.com/ZvBLxRv.png)

Pipline beschrijving geven en selecteren op welke manier verbinding wordt gemaakt (via api access token).

![](https://i.imgur.com/ZAEid2u.png)

Selecteren dat pipline script van een SCM (Git Source Management) komt. De error in onderstaande afbeelding is omdat GitLab nog geen SSH key heeft gedefinieerd van de Jenkins server.

![](https://i.imgur.com/JmwkqYN.png)

Repository van `*/master` vervangen naar `*/main`, script pad controleren en pipline opslaan.
![](https://i.imgur.com/BopH2r2.png)



**Resolutie pipline error (SSH key toevoegen in GitLab):**
Key pair aanmaken op de Jenkins-srv;
![](https://i.imgur.com/pLIvLWJ.png)

- `cd .ssh`
- `cat id_rsa.pub`
- Copy paste in GitLab ssh keys:
![](https://i.imgur.com/R9hmP5v.png)


De error blijft persisteren, mogelijks dat de Jenkins interface achterliggend de repository niet opnieuw gaat valideren. Daarom wordt de repo handmatig op de server gezet.

![](https://i.imgur.com/9lRoAtQ.png)
- `git ls-remote -h --git@gitlab.com:ikdoeict/gerrit.vanmol/automationplatform.git HEAD`
Voorgaand commando werd mee gegeven op de Jenkins interface
![](https://i.imgur.com/nJf96sY.png)

**Error bleef persisteren! Na wisselen van SSH naar HTTPS link en uitvoeren van mee gegeven commando in de terminal is de error weg gewerkt.**

![](https://i.imgur.com/M6lOtSp.png)
![](https://i.imgur.com/SJFejDu.png)

Builds bleven falen, probleem was dat het Jenkinsfile bestand was gedefinieerd in de Django app folder en niet in de root folder van de repository.

![](https://i.imgur.com/blHFspJ.png)
