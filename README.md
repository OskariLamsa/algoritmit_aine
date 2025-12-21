# algoritmit_aine

Tämä on Helsingin yliopiston kurssin Algoritmit ja Tekoäly Harjoitustyon palautus-repositorio
Projektini tarkoitus on havainnoida kahden polunetsijä algoritmin (Astar ja JPS) eroja.

## ohjeet

- Kun olet kloonannut repositorion, aja:
`poetry install --no-root`
- Jonka jälkeen voit testata algoritmia käyttöjärjestelmällä:
`poetry run invoke main`
- Kirjoita haluamasi algoritmin nimi, kuten astar. Sitten kirjoita haluamasi kartan nimi, kuten Paris_0. Kun pygame latautuu, ja näet kartan, paina vasemalla hiirinäppäimellä aloitus, ja lopetuspikselit kartalle (ne ovat todella pieniä). Sitten, paina Space ja katso, miten algoritmi löytää tien.
- Voit myos ajaa molemmat algoritmit kirjoittamalla all, ja voit myos piirtää oman kartan kirjoittamalla custom.
![kuva](https://i.imgur.com/CscqPUV.png)
## Testaus
- Voit ajaa testit komennolla:
`poetry run invoke test`
