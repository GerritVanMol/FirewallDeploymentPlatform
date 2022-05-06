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
- 'python3 -m venv my_platfrom' (nieuwe map maken)
- Alle bestanden van oude map (`.venv_platform`) naar nieuwe overmaken (`pmy_platform`)
- Omgeving opstarten `. myplatfrom/bin/activate`
- `pip3 install requirements.txt` (terug installeren van nodige packages)
___
### 7. Aanmaken deployment gebruiker

