# Loppuraportti

Tämän kurssin aikana opiskelin polunetsijä-algoritmien historiaa, ja koodasin kaksi hyvin suosittua polunetsijä algoritmia, A* ja JPS. Lisäksi testasin eroja niiden suorituksen nopeudessa.
Aloitin A* toteutuksesta ja käytin pygame-kirjastoa polunetsijoiden visualisointiin. Sitten tein skriptit map_encoder ja map_loader, joilla voi muuttaa karttakuvat csv -tiedostoiksi, ja sitten käyttää näitä tiedostoja poluissa.
Jump point searchin toteuttamisessa minulla oli vaikeuksia, sillä ymmärsin sen väärin monta kertaa. Lisäksi yksi lähteistäni antoi väärää informaatiota, joka sekoitti pääni viikon ajan.

### Mitä tuli opittua
A* ja JPS ovat loppujen lopuksi aika samanlaisia algoritmeja. JPS avaa nodeja samalla logiikalla kuin A*kin, mutta vähentää avoimeen listaan lisättyjen nodejen määrää merkittävästi tekemällä hyppyjä. Hypyt jatkuvat yhteen suuntaan niin kauan kunnes ne tormäävät seinään, tai kohtaavat pakotetun naapurin.
Tämä eteneminen on varsin nopeaa, sillä hypyn aikana lasketaan tarkistuksia O(1) ajassa. Onko tämä node seinä, onko vieressä pakotettu naapuri, jne. Itse open-setin operoiminen tapahtuu O(logn) ajassa, kun sinne laitetaan nodeja, ja kun sieltä haetaan halvin.
Koska noita operaatioita tehdään paljon, JPS tarjoaa nopeamman vaihtoehdon korvaamalla näitä O(logn) operaatioita yksinkertaisilla O(1) operaatoilla. JPS itse asiassa suorittaa enemmän operaatioita kuin A*, mutta koska muutama O(1) on niin paljon nopeampi kuin yksi O(logn), niin JPS on nopeampi

### A*
A*in vahvuus on implementaation helppoudessa. Mikäli polunetsijää on tarkoitus ajaa pienissä sovelluksissa, kuten vaikkapa pelissä jossa kartan koko on maksimissaan 100, niin se on täysin käypä algoritmi. Toinen vahvuus A*ila on se, että jos algoritmia ajetaan todella tiheässä tilassa, jossa polku vaatii paljon käännoksiä, niin sen nopeus JPS:ään verrattuna kasvaa.
A*in heikkous tietysti sen hitaus. Se ei ole optimaalinen valinta kartoille, joissa on paljon tyhjää tilaa. Mitä enemmän A*ille annetaan mahdollisuuksia lisätä irrelevantteja nodeja sen open-settiin, sitä hitaammaksi se tulee.
Tässä on esimerkki:
![A*_bad_example](https://i.imgur.com/68yLO92.png)

### JPS
JPS:n vahvuus on sen hypyissä. Mikäli kartta on sellainen, jossa JPS kykenee hyppimään pitkiä matkoja ennen kuin se saapuu seinään tai forced neighboriin, niin se korvaa monta open-set operaatiota nopeilla tarkistuksilla.
On kyllä totta, että JPS usein hyppii suuntiin, jotka eivät ole relevantteja. Esim aloitusnodesta kun lähdetään, meidän täytyy hypätä joka suuntaan, siinä missä A* lähtee liikkeelle välittomästi kohti maalin suuntaa sen heuristiikan mielestä, niin JPS sen sääntojen perusteella täytyy hypätä "turhiin" suuntiin jotka eivät ehkä ole lainkaan optimaalisen polun suunnassa. Lisäksi on mahdollista saavuttaa karttakoko, jolloin tyhjää tilaa niin paljon, että hypyt ovat esim 100000 nodea pitkiä, joka hidastaa algoritmia.
Kuitenkin nuo ovat melko teoreettisia huolia. Yleensä polunetsijäalgoritmeja ajetaan järkevillä kartoilla, jotka eivät ole niin isoja, että hypyt olisivat haitaksi.
Ylhäällä oleva kuva on todella hyvä esimerkki kartasta, jossa JPS:n teho käy ilmi, mutta voimme viedä tämän vielä pitemmälle seuraavassa testissä:
![JPS_good_example](https://i.imgur.com/EaXbP1r.png)
Tässä kartassa esteet ovat kovin neliskanttisia. Ne siis hädin tuskin tuottavat yhtään jump pointteja, joten tämä tilanne on JPSlle todella optimaalinen. Esteiden tiheyden ja sahalaitaisuuden kasvaessa algoritmi hidastuu.
Alhaalla esimerkki tästä:
![JPS_bad_example](https://i.imgur.com/ITS0ksj.png)
Tällä kartalla Astar ja JPS ovat suunnilleen yhtä nopeita. Huomattavaa on jump pointejen määrä suhteellisen pienellä kartalla. Kuten aiemmin tuli huomattua, JPS:n teho perustuu open-setin operaatioiden välttämiseen, joten jos niitä on tehtävä paljon niinkuin tässä esimerkissä, algoritmi lähestyy Astarin toimintaa.

### Testaus
Pytestillä suoritetut testit menevät kaikki läpi. Niissä testataan apuskriptejä, ja apufunktioita algoritmien sisällä. Mutta kiinnostavin niistä on algo_function_test, jossa testaamme, että Astar ja JPS toimivat oikein. Piirisin test_cardinals ja test_diagonals kartat, joissa testataan monipuolisesti algoritmien kykyä laskea optimaalinen reitti. Varmistaakseni, että orientaatiolla ei ole väliä, niin noista kartoista on saatavilla käännetyt versiot, 90, 180, ja 270 asteen kulmissa. Ajetaan siis kartta molemmilla algoritmeilla, ja kaikilla kartan orientaatioilla, ja varmistetaan, että niistä saadaan täysin sama optimaalinen polun pituus, jonka olen käsin laskenut.
Lisäksi testasin satunnaisesti algoritmien suoritusta isommilla kartoilla, jotka on saatavilla osoitteesta https://www.movingai.com/benchmarks/street/index.html
Minulla oli 30 karttaa, joten ajoin jokaisella kartalla 3 testiä per algoritmi, joten yhteensä 90 polkua molemmilla algoritmeilla. Varmistin myos, että valitsemme sellaiset aloitus- ja lopetuspisteet, että polun pituus on vähintään 500 pikseliä. Tämä testidata loytyy dokumentaatiokansiosta. Molemmat algoritmit palauttivat täysin yhtä pitkän polun, ja JPS oli joka kerralla nopeampi, joka oli odotettavissa.
Keskimäärin JPS oli 12.33 kertaa nopeampi kuin Astar.
