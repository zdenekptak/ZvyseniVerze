from verzeAutomat import VerzovaciAutomat

verzovaciAutomat = VerzovaciAutomat()
souboryKeKontrole = 'C:/Users/zdenek.ptak/Repository/CisloVerze/souborykekontrole.json'
iniSoubor = 'posledniUlozenaVerze.ini'
souborCommitSVN = 'commitSvn.bat'
uvodCesty = "C:\\HeO_vyroba_distribuce\\Zdroje"
cestyKeZdrojumFinal = {}
cestyKeZdrojum = {
    "Ostre": "\\Ostre\\asseco\\_Verze.inc",
    "Stare": "\\Stare\\asseco\\_Verze.inc", 
    "Freeze": "\\Freeze\\asseco\\_Verze.inc"
}
for zdroje, i in cestyKeZdrojum.items():
    cestyKeZdrojum[zdroje] = uvodCesty + i

vysledkyPoslednichZmen = verzovaciAutomat.jsouDnesZmenyVSouborech(souboryKeKontrole, uvodCesty)

for zdroje, cesta in cestyKeZdrojum.items():
    print(zdroje)
    if zdroje == 'Ostre':
        verzovaciAutomat.dokonceni(zdroje, cesta, iniSoubor, vysledkyPoslednichZmen, souborCommitSVN, uvodCesty)
            
    elif zdroje == 'Stare':
        verzovaciAutomat.dokonceni(zdroje, cesta, iniSoubor, vysledkyPoslednichZmen, souborCommitSVN, uvodCesty)
            
    else:
        verzovaciAutomat.dokonceni(zdroje, cesta, iniSoubor, vysledkyPoslednichZmen, souborCommitSVN, uvodCesty)