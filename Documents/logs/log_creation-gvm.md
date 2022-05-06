# Bachelorproef LOGBOEK

- **Server firewall updaten (activeren en poorten openen)**
    - `sudo ufw allow ssh`
    - `sudo ufw allow 80/tcp`
    - `sudo ufw allow 8080/tcp`
    - `sudo ufw status numbured` (controle open poorten)
        ![UFW Open poorten](https://i.imgur.com/U8JEAA3.png)

    - `sudo ufw enable` (firewall activeren bij opstart)
        ![Controle firewall enabled](https://i.imgur.com/W7xBTvJ.png)

       

- **Opstellen virtuele omgeving**
    - python3 versie controleren:
    ![Python3 versie controle](https://i.imgur.com/ZdV00lZ.png)

    - `sudo apt install python3-venv` (ondersteuning voor virtuele omgevingen)
    - `python3 -m venv .venv-platform` (maken folder in virtuele omgeving)
    - `. .venv-platform/bin/activate` (activeren => kan alleen in folder waar virtuele omgeving map staat)
        ![Controle activatie venv omgeving](https://i.imgur.com/cZ2LS65.png)


    - `deactivate` (omgeving stoppen)

- **Installeren van Django in virtuele omgeving**
    - `pip3 install django`
    - `python 3 -m django --verion` (controle succesvolle installatie)
    ![Django versie controle](https://i.imgur.com/RicYiYl.png)

        ~~`sudo apt install python3-django`~~    
- **Installeren van extra packages (voor los koppelen van "env" omgeving variabelen)**
    - `pip3 install python-decouple`
    Package zal er voor zorgen dat paswoorden en secret keys niet worden mee vertaald naar de productie versie. Deze package zal er ook voor zorgen dat confidentiele data niet worden mee genomen daar een Git repository.

- **Creeren van project structuur (in virtuele omgeving folder)**
    - `cd .venv-platform`
    - `django-admin startproject siteplatform`
        ![Controle project in juiste (venv) folder](https://i.imgur.com/WHN0QU9.png)


- **Activeren Django site (test)**
    - `cd` naar project folder (`siteplatform`)
    - `ls` voor controle projet inhoud
    ![Controle project inhoud](https://i.imgur.com/yw6KfEF.png)

- **Foutmelding (geen migraties voor de databank)!**
    ![Error geen migraties](https://i.imgur.com/pfH8KNw.png)    
    Resolutie: `python3 manage.py migrate`


    - `python3 manage.py runserver 10.0.89.147:8080` (starten dev server)

- **Foutmelding (geen hosts toegelaten tot server)**
    ![Error host disallowed](https://i.imgur.com/6j0fPP8.png)
    Resolutie: voeg `'*'` toe aan `ALLOWED_HOSTS[]` in `~/siteplatform/settings.py`

    ![ALLOWED_HOSTS var in settings.py](https://i.imgur.com/ItHZ5N7.png)
     
     - `python3 manage.py runserver 10.0.89.147:8080` (starten dev server)
![Django default succes site](https://i.imgur.com/4BYTs25.png)


- **Copy maken van nodige packages**
    - `pip3 freeze > requirements.txt`