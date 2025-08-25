# Saliohjelma

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen harjoitteita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään harjoitteita.
* Käyttäjä näkee sovellukseen lisätyt harjoitteet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät harjoitteet.
* Käyttäjä pystyy etsimään harjoitteita hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä harjoitteita.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän harjoittelutilastoja ja käyttäjän lisäämät harjoitteet.
* Käyttäjä pystyy valitsemaan harjoitteelle toistojen kuvauksen, toistojen määrän, mahdollisen painon ja sarjojen määrän.
* Jokaiseen harjoitteeseen on yhdistetty tilastot: kuinka monta kertaa sarja on tehty ja milloin

## Sovelluksen asennus

Asenna riippuvuudet

```bash
pip install -r requirements.txt
```

Luo ja alusta tietokanta (WIP)

```bash
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

Käynnistä sovellus

```bash
flask run
````

