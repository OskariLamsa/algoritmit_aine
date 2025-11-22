### Viikkoraportti 4
Tällä viikolla laajensin projektia paljon. Ensinnäkin, huomasin miten pygame hidastui huomattavasti kartan koon kasvaessa. Jo 256*256 kartat oli kestämättömän hitaita ajaa. Ongelma oli siinä, miten paljon roskaa piirrämme joka framella. (Valkoinen tausta, jokainen spot...). Nyt, tausta piirretään vain kerran, linjat spottejen välillä on poistettu, ja nyt yritämme piirtää vain uusia pikseleitä, ja skippaamme jo edellisellä framella piirretyt. Vizualizer luokkaa voi varmasti parantaa entisestään, mutta nyt kaikki 1073x1073 kartat voidaan ajaa hyväksyttävän nopeasti.

Algoritmeille on nyt oma kansio.
Karttakuvat ovat maps-kansiossa.
.csv data karttakuvista maps_data kansiossa.
map_encoder.py muuttaa karttakuvat .csv dataksi.
(Jos kiinnostaa kokeilla, poista maps_data-kansion tiedostot, ja aja poetry run python map_encoder.py)
map_loader.py muuttaa .csv tiedoston listaksi pikseleitä.
visualizer nyt osaa vastaanottaa pikselilistan, ja piirtää esteitä sen mukaan.
main.py luotu, joka on kuin käyttöjärjestelmä algojen demoamiseen.

Lisäksi testaaminen on aloitettu. map_encoder-tiedostolla on kolme testiä.

Nyt projekti on siinä pisteessä, että voimme ajaa algoritmeilla kartoissa, ja visualizer on sen verran nopea, että 1073*1073 kartat voidaan ajaa kivutta. Testaaminenkin on alkanut.
Jump-point-searchiä en saanut vielä aloitettua, kun näissä muissa asioissa meni sen verran kauan. Mutta nyt projekti on mainiolla mallilla. Alan implementoimaan JPS heti ensi viikon alussa. Sanottiin, että on hyvin mahdollista, että teen sen väärin ja tarvitsen viikkopalautteen sen korjaamiseen, niin aion kysyä apua Telegrammista viikon aikana, jospa se auttaisi.

Tällä viikolla töitä tehty 11 tuntia