# Saliohjelma

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen harjoitteita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään harjoitteita.
* Käyttäjä näkee sovellukseen lisätyt harjoitteet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät harjoitteet.
* Käyttäjä pystyy etsimään harjoitteita hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä harjoitteita.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän harjoittelutilastoja ja käyttäjän lisäämät harjoitteet.
* Käyttäjä pystyy valitsemaan harjoitteelle toistojen kuvauksen, toistojen määrän, mahdollisen painon ja sarjojen määrän.
* Jokaiseen harjoitteeseen on yhdistetty tilastot: kuinka monta kertaa sarja on tehty ja milloin

## Sovelluksen ajaminen

Ensin .env-tiedosto

1. Kopioi `.env.example` tiedostoon `.env`
2. Luo `SECRET_KEY` ajamalla komento
```bash
python ./scripts/create_key.py
```
2. Kopioi saamasi avain ja talleta se muuttujalle `SECRET_KEY`

Sen jälkeen voit ajaa sovelluksen. Elämää helpottaaksesi voit ajaa skriptin `run-app.sh`, joka asentaa kaikki riippuvuudet, alustaa tietokannan, jos sitä ei ole olemassa (WIP) ja käynnistää sovelluksen. Vaihtoehtoisesti voit tehdä kaikki vaiheet erikseen:

1. Asenna riippuvuudet

```bash
pip install -r requirements.txt
```

2. Luo ja alusta tietokanta (WIP)

```bash
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

3. Käynnistä sovellus

```bash
flask run
```

## Dev mode

Jos haluat hot reloadin ja nähdä kattavampia debug lokeja, aja

```bash
./run-app.sh --dev
```