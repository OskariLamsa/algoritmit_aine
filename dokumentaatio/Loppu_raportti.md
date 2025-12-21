# Loppu Raportti

Tämän kurssin aikana opiskelin polunetsijä-algoritmien historiaa, ja koodasin kaksi hyvin suosittua polunetsijä algoritmia, A* ja JPS. Lisäksi testasin eroja niiden suorituksen nopeudessa.
Aloitin A* toteutuksesta ja käytin pygame-kirjastoa polunetsijoiden visualisointiin. Sitten tein skriptit map_encoder ja map_loader, joilla voi muuttaa karttakuvat csv -tiedostoiksi, ja sitten käyttää näitä tiedostoja poluissa.
Jump point searchin toteuttamisessa minulla oli vaikeuksia, sillä ymmärsin sen väärin monta kertaa. Lisäksi yksi lähteistäni antoi väärää informaatiota, joka sekoitti pääni viikon ajan.

### Mitä tuli opittua
A* ja JPS ovat loppujen lopuksi aika samanlaisia algoritmeja. JPS avaa nodeja samalla logiikalla kuin A*kin, mutta vähentää avoimeen listaan lisättyjen nodejen määrää merkittävästi tekemällä hyppyjä. Hypyt jatkuvat yhteen suuntaan niin kauan kunnes ne tormäävät seinään, tai kohtaavat pakotetun naapurin.
Tämä eteneminen on varsin nopeaa, sillä hypyn aikana lasketaan tarkistuksia O(1) ajassa. Onko tämä node seinä, onko vieressä pakotettu naapuri, jne. Itse open setin operoiminen tapahtuu O(logn) ajassa, kun sinne laitetaan nodeja, ja kun sieltä haetaan halvin.
Koska noita operaatioita tehdään paljon, JPS tarjoaa nopeamman vaihtoehdon korvaamalla näitä O(logn) operaatioita yksinkertaisilla O(1) operaatoilla. JPS itse asiassa suorittaa enemmän operaatioita kuin A*, mutta koska muutama O(1) on niin paljon nopeampi kuin yksi O(logn), niin JPS on nopeampi

## A*
A*in vahvuus on implementaation helppoudessa. Mikäli polunetsijää on tarkoitus ajaa pienissä sovelluksissa, kuten vaikkapa pelissä jossa kartan koko on maksimissaan 100, niin se on täysin käypä algoritmi. Toinen vahvuus A*ila on se, että jos algoritmia ajetaan todella tiheässä tilassa, jossa polku vaatii paljon käännoksiä, niin sen nopeus JPS:ään verrattuna kasvaa.
A*in heikkous tietysti sen hitaus. Se ei ole optimaalinen valinta kartoille, joissa on paljon tyhjää tilaa. Mitä enemmän A*ille annetaan mahdollisuuksia lisätä irrelevantteja nodeja sen open settiin, sitä hitaammaksi se tulee.
Tässä on esimerkki:
![A*_bad_example](https://i.imgur.com/68yLO92.png)

### JPS
JPS:n vahvuus on sen hypyissä. Mikäli kartta on sellainen, jossa JPS kykenee hyppimään pitkiä matkoja ennen kuin se saapuu seinään tai forced neighboriin, niin se korvaa monta open-set operaatiota nopeilla tarkistuksilla.
On kyllä totta, että JPS usein hyppii suuntiin, jotka eivät ole relevantteja. Esim aloitusnodesta kun lähdetään, meidän täytyy hypätä joka suuntaan, siinä missä A* lähtee liikkeelle välittomästi kohti maalin suuntaa sen heuristiikan mielestä.
Toisaalta juuri tämä 
