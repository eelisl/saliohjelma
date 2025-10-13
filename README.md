# Saliohjelma

Saliohjelma-sovellus on MVP ohjelma saliharjoitteluun. Sovelluksen avulla pystyt lisäämään, poistamaan ja muokkaamaan omia harjoitteitasi omaan ohjelmaan. "Harjoittele"-kohdassa voit merkitä harjoituksia tehdyksi esimerkiksi salilla käynnin aikana, harjoitusten nollaantuessa automaattisesti päivän päätteeksi. Voit lisäksi nähdä inspiraatioksi muiden tekemiä harjoitteita ja tarvittaessa korjata harjoitteiden kategorioita. Omassa profiilissasi näet mielenkiintoista statistiikkaa harjoituksistasi.

## Sovelluksen toiminnot

-   Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
-   Käyttäjä pystyy lisäämään sovellukseen harjoitteita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään harjoitteita.
-   Käyttäjä näkee sovellukseen lisätyt harjoitteet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät harjoitteet.
-   Käyttäjä pystyy etsimään harjoitteita hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä harjoitteita.
-   Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän harjoittelutilastoja ja käyttäjän lisäämät harjoitteet.
-   Käyttäjä pystyy valitsemaan harjoitteelle toistojen kuvauksen, toistojen määrän, mahdollisen painon ja sarjojen määrän.
-   Jokaiseen harjoitteeseen on yhdistetty tilastot: kuinka monta kertaa sarja on tehty ja milloin

## Sovelluksen ajaminen

Elämää helpottaaksesi voit ajaa skriptin `run-app.sh --init`, joka asentaa kaikki riippuvuudet, alustaa tietokannan, jos sitä ei ole olemassa ja käynnistää sovelluksen. Vaihtoehtoisesti voit tehdä kaikki vaiheet erikseen:

1. Asenna riippuvuudet

```bash
pip install -r requirements.txt
```

2. Luo ja alusta tietokanta

```bash
sqlite3 database.db < ./database/schema.sql
sqlite3 database.db < ./database/init.sql
```

3. Käynnistä sovellus

```bash
flask run
```

4. Lisää dataa tietokantaan (valinnainen)

```bash
python ./database/seed.py
```

## Dev mode

Jos haluat hot reloadin ja nähdä kattavampia debug lokeja, aja

```bash
./run-app.sh --dev
```

## Tuotannossa

Jos aiot ajaa sovelluksen tuotantoympäristössä, sinun täytyy luoda `SECRET_KEY` tiedostoon `config.py`. Apuna voit käyttää `./scripts/create_key.py` skriptiä. Kopioi tulostettu arvo configiin.

Oikeassa elämässä suosittaisin käyttämään `.env` muuttujia (minkä jo kerran implementoin, ennen kuin tajusin, että ulkoisia kirjastoja ei saa käyttää), mikä on alan standardi tapa säilyttää sovelluksen salaisuuksia.

## Sovelluksen toiminta suurilla tietomäärillä

Sovellusta on testattu suurella tietomäärällä. Voit kokeilla itse ajamalla `python ./database/seed.py` initialisoinnin jälkeen.

Kun tietokannassa on dataa, voit kirjautua käyttäjällä `user1`, salasana `user1_password`.

Profiilin data on sivutettu ja stats data indeksoitu. Data latautuu nopeasti, konsoli näyttää, että yhden haun kesto on 0.0s.

Samoin /harjoitteet -sivun kaikki harjoitteet on sivutettu. Data latautuu nopeasti, konsoli näyttää, että yhden haun kesto on 0.0s.

## Linttaus

Katso [PYLINT_REPORT.md](PYLINT_REPORT.md)