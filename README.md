# EPSI WorkShop 2022

## Dossier "workshop_serveur"
Contient le code du serveur de trading.

Pour le lancer:
```sh
>>> python3 serveur.py {port}

>>> python3 serveur.py 1233
```


## Dossier "workshop_client":
Contient le code test client.

Pour le lancer:
```sh
>>> python3 main.py {ip}:{port} {indentifiant/pays}

>>> python3 main.py 127.0.0.1:1233 FRA
```


## Dossier "workshop_logchecker":
Contient le code de l'afficheur de log, se connectant au socker ouvert sur {IP}:7777

Pour le lancer:
```sh
>>> python3 main.py
```
