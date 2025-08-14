# Web Scraper App

## Zweck der App
Die Web Scraper App liest Daten von der smard-API der Bundesnetzagentur aus und speichert diese in einer MariaDB-Datenbank ab. Der Endpunkt der API ist [https://www.smard.de/app](https://www.smard.de/app). Über die API lassen sich Timestamps und Zeitreihendaten über einfache GET-Requests ohne Query-String anfragen. Ergebnisse werden über Pfad-Parameter (im Folgenden in geschweiften Klammern) gefiltert.

## Hauptfunktionen
1. **Datenabruf alle 15 Minuten**: Die App ruft alle 15 Minuten Daten von der smard-API ab.
2. **Datenverarbeitung**: Die API hat ein sehr unschönes Design, sodass pro Abruf alle Daten immer in einem Zeitfenster von einer Woche (Sonntag-Sonntag) geliefert werden. Für alles, was noch in Zukunft liegt, gibt es null-Werte. Die App verarbeitet immer die 5 neuesten (nicht-null) Einträge, die die API liefert.
3. **Datenbankintegration**: Vor dem Schreiben in die Datenbank wird geprüft, ob für einen Timestamp bereits Werte enthalten sind. Falls nicht, werden die neuen Werte eingetragen.

## Datenbankzugangsdaten
- **Hostname**: web-scraper-mariadb
- **Port**: 3306
- **Username**: root
- **Passwort**: password
- **Datenbank**: powerdata

## Tabellen (in [models.py](./app/models.py) beschrieben)
1. **powertypemapping**: Mapping von Nummer zu Beschreibung für bestimmten Typ.
2. **consumption**: Daten über den Stromverbrauch je Region und Typ in `MWh`.
3. **generation**: Daten über die Stromerzeugung je Region und Typ in `MWh`.

## Installationsanweisungen
- **Minikube und Docker**: Diese müssen installiert sein.

## Verwendung
Um die App zu verwenden, führen Sie den folgenden Befehl aus:
```sh
./deploy.sh
```
