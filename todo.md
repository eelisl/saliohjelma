## Perustoiminnot

[X] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
[X] Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita
[X] Käyttäjä näkee sovellukseen lisätyt tietokohteet
[ ] Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella
[ ] Käyttäjäsivu näyttää tilastoja ja käyttäjän lisäämät tietokohteet
[ ] Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun
[ ] Käyttäjä pystyy lisäämään tietokohteeseen toissijaisia tietokohteita

## Perusvaatimukset

[ ] Sovellus toteutettu kurssimateriaalin mukaisesti
[X] Sovellus toteutettu Pythonilla käyttäen Flask-kirjastoa
[X] Sovellus käyttää SQLite-tietokantaa
[X] Kehitystyössä käytetty Gitiä ja GitHubia
[X] Sovelluksen käyttöliittymä muodostuu HTML-sivuista
[X] Sovelluksessa ei ole käytetty JavaScript-koodia
[X] Tietokantaa käytetään suoraan SQL-komennoilla (ei ORMia)
[X] Flaskin lisäksi käytössä ei muita erikseen asennettavia Python-kirjastoja
[X] Sovelluksen ulkoasu (HTML/CSS) on toteutettu itse ilman kirjastoja

## Käytettävyys

[ ] Sovelluksen perustoiminnot toimivat
[X] CSS:n avulla toteutettu ulkoasu (itse tehty, ei CSS-kirjastoa)
[ ] Sovellusta on helppoa ja loogista käyttää
[ ] Käyttäjän lähettämässä tekstissä rivinvaihdot näkyvät selaimessa
[ ] Kuvissa käytetty alt-attribuuttia (jos sovelluksessa kuvia)
[X] Lomakkeissa käytetty label-elementtiä

## Versionhallinta

[X] Kehitystyön aikana on tehty commiteja säännöllisesti
[X] Commit-viestit on kirjoitettu englanniksi
[X] Tiedosto README.md kertoo, millainen sovellus on ja miten sitä voi testata
[X] Versionhallinnassa ei ole sinne kuulumattomia tiedostoja
[X] Commitit ovat hyviä kokonaisuuksia ja niissä on hyvät viestit

## Ohjelmointityyli

[X] Koodi on kirjoitettu englanniksi
[X] Muuttujat ja funktiot nimetty kuvaavasti
[X] Sisennyksen leveys on neljä välilyöntiä
[X] Koodissa ei ole liian pitkiä rivejä
[X] Muuttujien ja funktioiden nimet muotoa total_count (ei totalCount)
[X] Välit oikein =- ja ,-merkkien ympärillä
[X] Ei ylimääräisiä sulkeita if- ja while-rakenteissa

## Tietokanta

[X] Taulut ja sarakkeet on nimetty englanniksi
[X] Taulut ja sarakkeet on nimetty kuvaavasti
[X] Käytetty REFERENCES-määrettä, kun viittaus toiseen tauluun
[X] Ei kyselyjä muotoa SELECT \*
[X] Kaikki tiedot haetaan yhdellä SQL-kyselyllä, jos järkevästi mahdollista
[X] Koodissa ei tehdä asioita, jotka voi mielekkäästi tehdä SQL:ssä
[X] Käytetty try/except SQL-komennon ympärillä vain aiheellisesti

## Turvallisuus

[X] Salasanat tallennetaan tietokantaan asianmukaisesti
[X] Käyttäjän oikeus nähdä sivun sisältö tarkastetaan
[X] Käyttäjän oikeus lähettää lomake tarkastetaan
[ ] Käyttäjän syötteet tarkastetaan ennen tietokantaan lisäämistä
[X] SQL-komennoissa käytetty parametreja
[X] Sivut muodostetaan sivupohjien kautta
[ ] Lomakkeissa on estetty CSRF-aukko

## Testaus

[ ] Sovellusta testattu suurella tietomäärällä ja raportoitu tulokset
[ ] Sovelluksessa käytössä tietokohteiden sivutus
[ ] Tietokantaan lisätty indeksi, joka nopeuttaa suuren tietomäärän käsittelyä
