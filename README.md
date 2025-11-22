# algoritmit_aine

Tämä on Helsingin yliopiston kurssin Algoritmit ja Tekoäly Harjoitustyon palautus-repositorio

## ohjeet

- Kun olet kloonannut repositorion, aja:
`poetry install --no-root`
- Jonka jälkeen voit testata algoritmia käyttöjärjestelmällä:
`poetry run invoke main`
- Kirjoita haluamasi algoritmin nimi, kuten astar. Sitten kirjoita haluamasi kartan nimi, kuten Paris_0. Kun pygame latautuu, ja näet kartan, paina vasemalla hiirinäppäimellä aloitus, ja lopetuspikselit kartalle (ne ovat todella pieniä). Sitten, paina Space ja katso, miten algoritmi löytää tien.
![kuva](https://i.imgur.com/CscqPUV.png)
## Testaus
- Voit ajaa testit komennolla:
`poetry run invoke test`
