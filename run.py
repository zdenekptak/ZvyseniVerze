from verzeAutomat import VerzovaciAutomat

verzovaciAutomat = VerzovaciAutomat()
souboryKeKontrole = "C:/Users/zdenek.ptak/Repository/CisloVerze/souborykekontrole.json"
iniSoubor = "C:/Users/zdenek.ptak/Repository/CisloVerze/posledniUlozenaVerze.ini"
souborCommitSVN = "C:/Users/zdenek.ptak/Repository/CisloVerze/commitSvn.bat"
uvodCesty = "C:\\HeO_vyroba_distribuce\\Zdroje"
konecCestyKeZdrojum = {
    "Ostre": "\\Ostre\\asseco\\_Verze.inc",
    "Stare": "\\Stare\\asseco\\_Verze.inc", 
    "Freeze": "\\Freeze\\asseco\\_Verze.inc"
}

celeCestyKeZdrojum = {}
for zdroje, konecCesty in konecCestyKeZdrojum.items():
    # update z SVN
    verzovaciAutomat.updateFromSVN(zdroje)
    celeCestyKeZdrojum[zdroje] = uvodCesty + konecCesty


vysledkyPoslednichZmen = verzovaciAutomat.jsouDnesZmenyVSouborech(souboryKeKontrole, uvodCesty)

for zdroje, cesta in celeCestyKeZdrojum.items():
    if zdroje == 'Ostre':
        verzovaciAutomat.dokonceni(zdroje, cesta, iniSoubor, vysledkyPoslednichZmen, souborCommitSVN, uvodCesty)
            
    elif zdroje == 'Stare':
        verzovaciAutomat.dokonceni(zdroje, cesta, iniSoubor, vysledkyPoslednichZmen, souborCommitSVN, uvodCesty)
            
    else:
        verzovaciAutomat.dokonceni(zdroje, cesta, iniSoubor, vysledkyPoslednichZmen, souborCommitSVN, uvodCesty)
