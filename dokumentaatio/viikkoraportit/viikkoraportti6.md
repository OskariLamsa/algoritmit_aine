### Viikkoraportti 6
Tällä viikolla sain viimeinkin Jump point searchin toimimaan. Ongelmana oli, että viime viikkojen aikana olin yksinkertaisesti ymmärtänyt sen väärin. Tämä on hankalin koodaus-pulma, minkä olen elämässäni taklannut. Osoitteessa https://zerowidth.com/2013/a-visual-explanation-of-jump-point-search/#try-it-out oleva ohjeistus oli hyvä, mutta siinä on yksi vika. "Tying it together" otsikon alla kuvistetussa ohjeistuksessa ![kuva](https://i.imgur.com/uazF72B.png) kuvassa neljä lukee "Lastly, we expand diagonally, finding nothing because we bump into the edge of the map.", mikä on tietääkseni väärin. Et saa jatkaa diagonaalista hyppyä, jos kardinaali löysi jump pointin.

Nyt kun JPS toimii täydellisesti, niin aion isolla kiireellä tehdä testit, ja koodata tavan ajaa molemmat algoritmini samalla kartalla, jotta niiden nopeutta voi verrata helposti, ilman että tarvitsee ajaa molemmat erikseen.

Nyt on lisätty pieni aika raportti konsoliin, joka kertoo miten kauan algoritmin ajamisessa (ja pygamen värityksessä) kesti.

Tällä viikollä tein noin 20 tuntia töitä
