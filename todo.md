## Perustoiminnot

[ ] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
[ ] Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteitan
[ ] Käyttäjä näkee sovellukseen lisätyt tietokohteet
[ ] Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella
[ ] Käyttäjäsivu näyttää tilastoja ja käyttäjän lisäämät tietokohteet
[ ] Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun
[ ] Käyttäjä pystyy lisäämään tietokohteeseen toissijaisia tietokohteita

## Perusvaatimukset

[ ] Sovellus toteutettu kurssimateriaalin mukaisesti
[ ] Sovellus toteutettu Pythonilla käyttäen Flask-kirjastoa
[ ] Sovellus käyttää SQLite-tietokantaa
[ ] Kehitystyössä käytetty Gitiä ja GitHubia
[ ] Sovelluksen käyttöliittymä muodostuu HTML-sivuista
[ ] Sovelluksessa ei ole käytetty JavaScript-koodia
[ ] Tietokantaa käytetään suoraan SQL-komennoilla (ei ORMia)
[ ] Flaskin lisäksi käytössä ei muita erikseen asennettavia Python-kirjastoja
[ ] Sovelluksen ulkoasu (HTML/CSS) on toteutettu itse ilman kirjastoja

## Käytettävyys

[ ] Sovelluksen perustoiminnot toimivat
[ ] CSS:n avulla toteutettu ulkoasu (itse tehty, ei CSS-kirjastoa)
[ ] Sovellusta on helppoa ja loogista käyttää
[ ] Käyttäjän lähettämässä tekstissä rivinvaihdot näkyvät selaimessa
[ ] Kuvissa käytetty alt-attribuuttia (jos sovelluksessa kuvia)
[ ] Lomakkeissa käytetty label-elementtiä

## Versionhallinta

[ ] Kehitystyön aikana on tehty commiteja säännöllisesti
[ ] Commit-viestit on kirjoitettu englanniksi
[ ] Tiedosto README.md kertoo, millainen sovellus on ja miten sitä voi testata
[ ] Versionhallinnassa ei ole sinne kuulumattomia tiedostoja
[ ] Commitit ovat hyviä kokonaisuuksia ja niissä on hyvät viestit

## Ohjelmointityyli

[ ] Koodi on kirjoitettu englanniksi
[ ] Muuttujat ja funktiot nimetty kuvaavasti
[ ] Sisennyksen leveys on neljä välilyöntiä
[ ] Koodissa ei ole liian pitkiä rivejä
[ ] Muuttujien ja funktioiden nimet muotoa total_count (ei totalCount)
[ ] Välit oikein =- ja ,-merkkien ympärillä
[ ] Ei ylimääräisiä sulkeita if- ja while-rakenteissa

## Tietokanta

[ ] Taulut ja sarakkeet on nimetty englanniksi
[ ] Taulut ja sarakkeet on nimetty kuvaavasti
[ ] Käytetty REFERENCES-määrettä, kun viittaus toiseen tauluun
[ ] Ei kyselyjä muotoa SELECT \*
[ ] Kaikki tiedot haetaan yhdellä SQL-kyselyllä, jos järkevästi mahdollista
[ ] Koodissa ei tehdä asioita, jotka voi mielekkäästi tehdä SQL:ssä
[ ] Käytetty try/except SQL-komennon ympärillä vain aiheellisesti

## Turvallisuus

[ ] Salasanat tallennetaan tietokantaan asianmukaisesti
[ ] Käyttäjän oikeus nähdä sivun sisältö tarkastetaan
[ ] Käyttäjän oikeus lähettää lomake tarkastetaan
[ ] Käyttäjän syötteet tarkastetaan ennen tietokantaan lisäämistä
[ ] SQL-komennoissa käytetty parametreja
[ ] Sivut muodostetaan sivupohjien kautta
[ ] Lomakkeissa on estetty CSRF-aukko

## Testaus

[ ] Sovellusta testattu suurella tietomäärällä ja raportoitu tulokset
[ ] Sovelluksessa käytössä tietokohteiden sivutus
[ ] Tietokantaan lisätty indeksi, joka nopeuttaa suuren tietomäärän käsittelyä
