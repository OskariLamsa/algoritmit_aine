# Määrittelydokumentti

### Aihe

Tämän projektin aihe on polunetsintä-algoritmien tehokkuuden arvointi 2-uloitteisessa ruudukossa, olettaen, että ruudukossa matkustava algoritmi kykenee linnunkatseen tavoin näkemään koko ruudukon ylhäältä katsottuna. Ei siis mitään "fog of war" kaltaista informaation rajoitetta. Haluan vertailla 3 eri algoritmia, ja arvioida niiden tehokkuutta, ja minkälaisissa tilanteissa kukin on hyvä ratkaisu, ja milloin huono.

### Kieli

Toteutus pythonilla. Visuaalisesti algoritmien eteneminen voidaan näyttää pygame-kirjastolla. Testaus pylint-kirjastolla. Vertaisarvoinnin osalta mainittakoon, että tunnen myos Haskellia.

### Algoritmit

Vertailen kolmea eri algoritmia, A*, JPS ja Theta*, sillä ne kaikki lähestyvät tätä ongelmaa eri näkokulmista.

### Ohjelman syotteet

Jokaiselle algoritmille annetaan samat ruudukot ratkaistavaksi. Ruudukon informaatio esitetään "täydellisesti", eli ruudukko ei muutu suorituksen aikana, ja kaikki relevantti tieto on saatavilla ennen ensimmäistä liikettä. Ruudukko koostuu ruuduista, joista yksi on aloituspiste, toinen on lopetuspiste, ja loput ovat tyhjiä ruutuja, tai estettyjä ruutuja, joihin ei voi liikkua.

### Ydin

Tämän projektin ydin on näiden kolmen reitinhakualgoritmin tehokkuuden arviointi. Lisäksi haluan loytää ruudukkoja, jota nostattavat esille algoritmien vahvuudet, ja heikkoudet. Vaikka tietty algoritmi on yleisesti "parempi" kuin muut, niin toinen saattaa olla keskiarvollisesti parempi, jos odotat tietynlaisten ruudukoiden olevan muita yleisempiä.

### Lähteet

Lähteinä alustavasti aion käyttää ainakin:
https://zerowidth.com/2013/a-visual-explanation-of-jump-point-search
https://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf
https://www.youtube.com/watch?v=NmM4pv8uQwI
https://www.youtube.com/watch?v=JtiK0DOeI4A

### Lisäksi

Koska nämä kaikki ovat tunnettuja algoritmeja ja niiden dokumentaatio on helposti saatavilla, niin niiden aika-vaativuus on helppo tarkistaa. Minun osaltani kuitenkin minun on itse omin sanoin kyettävä kertomaan miksi esimerkiksi jokin algoritmi toimii O(n) ajassa.

Olen Tietojenkäsittelytieteen kandin opiskelija.
Projektin dokumentaation kieli on Suomi.
