from stat import S_ISREG, ST_CTIME, ST_MODE, ST_MTIME, ST_GID
import os, sys, time
from datetime import datetime
import json
import subprocess
from configparser import ConfigParser

class VerzovaciAutomat:
    def __init__(self):
        pass

    def denSouboruVAdresari(self, cestaKAdresari):
        self.cestaKAdresari = cestaKAdresari
        #  získame všechny soubory v adresáři s/ statistikami (fn jsou jednotlive soubory)
        seznamSouboruKeKontrole = [os.path.join(self.cestaKAdresari, fn) for fn in os.listdir(self.cestaKAdresari)]

        seznamStatCesta = [(os.stat(path), path) for path in seznamSouboruKeKontrole]
        # ponechat pouze běžné soubory, vložit datum vytvoření ((stat[ST_MTIME] - vlozi datum posledni zmeny)
        serazeneSoubory = ((stat[ST_MTIME], path) for stat, path in seznamStatCesta if S_ISREG(stat[ST_MODE]))    
        # smycka ktera vrati posledni modifikovny soubor
        for cdate, path in sorted(serazeneSoubory, reverse=True):

            datumSouboru = time.ctime(cdate)        
            ts = datetime.fromtimestamp(cdate).strftime('%Y-%m-%d')

            datumSouboruDen = [int(s) for s in datumSouboru.split() if s.isdigit()][0]

            return ts

    def jsouDnesZmenyVSouborech(self, configCesty, uvodCesty):
        self.configCesty = configCesty
        self.uvodCesty = uvodCesty

        # prace s json soubory
        with open(self.configCesty) as json_file:

            self.configCesty = json.load(json_file)

        # vytvoreni prazdnych slovniku pro zaznamenani posledni zmeny souboru
        verzovaciAutomat = VerzovaciAutomat()
        seznamVsechZmenOstre = []
        seznamVsechZmenStare = []
        seznamVsechZmenFreeze = []
        vsechnyZmenyOstre = {}
        vsechnyZmenyStare = {}
        vsechnyZmenyFreeze = {}
        # smycka pres vsechny adresare ktere kontrolujeme
        for zdroje, slovnikVyvoj in self.configCesty.items():

            if zdroje == 'Ostre':
                for vyvoj, cestaKonec in slovnikVyvoj.items():                
                    cesta = self.uvodCesty + cestaKonec 
                    seznamVsechZmenOstre.append((verzovaciAutomat.denSouboruVAdresari(cesta)))
                    vsechnyZmenyOstre[vyvoj] = verzovaciAutomat.denSouboruVAdresari(cesta)                
            if zdroje == 'Stare':                                                                                        
                for vyvoj, cestaKonec in slovnikVyvoj.items():
                    cesta = self.uvodCesty + cestaKonec
                    seznamVsechZmenStare.append(verzovaciAutomat.denSouboruVAdresari(cesta))
                    vsechnyZmenyStare[vyvoj] = verzovaciAutomat.denSouboruVAdresari(cesta)               
            if zdroje == 'Freeze':
                for vyvoj, cestaKonec in slovnikVyvoj.items():                    
                    cesta = self.uvodCesty + cestaKonec
                    seznamVsechZmenFreeze.append(verzovaciAutomat.denSouboruVAdresari(cesta))
                    vsechnyZmenyFreeze[vyvoj] = verzovaciAutomat.denSouboruVAdresari(cesta)

        seznamVsechZmen = {"Ostre" : seznamVsechZmenOstre, "Stare" : seznamVsechZmenStare, "Freeze" : seznamVsechZmenFreeze}                                         
        nowDate = datetime.now()  # current date and time
        datumDnesniDen = nowDate.strftime('%Y-%m-%d')
        print(f"Dnesni datum je: {datumDnesniDen}")
        print()
        for z, zmeny in seznamVsechZmen.items():
    #         print(zmeny)
            print(f'Datum posledni zmeny v {z}: {max(zmeny)}')
            print()


        konecneVysledky = {}
        if datumDnesniDen == max(seznamVsechZmenOstre):
            konecneVysledky['Ostre'] = True
        else:
            konecneVysledky['Ostre'] = False

        if datumDnesniDen == max(seznamVsechZmenStare):
            konecneVysledky['Stare'] = True
        else:
            konecneVysledky['Stare'] = False

        if datumDnesniDen == max(seznamVsechZmenFreeze):
            konecneVysledky['Freeze'] = True
        else:
            konecneVysledky['Freeze'] = False

        konecneVysledkyAnoNe = {}
        for z, anone in konecneVysledky.items():
            if z == 'Ostre':
                if anone == True:
                    konecneVysledkyAnoNe[z] = "Ano"
                else:
                    konecneVysledkyAnoNe[z] = "Ne"
            elif z == 'Stare':
                if anone == True:
                    konecneVysledkyAnoNe[z] = "Ano"
                else:
                    konecneVysledkyAnoNe[z] = "Ne"
            elif z == 'Freeze':
                if anone == True:
                    konecneVysledkyAnoNe[z] = "Ano"
                else:
                    konecneVysledkyAnoNe[z] = "Ne"

        print(f'Byly dnes zmeneny zdroje: {konecneVysledkyAnoNe}')
        print()
        return konecneVysledky


    def aktualniVerzeSVN(self, soubor):
        self.soubor = soubor
        with open(self.soubor, 'r') as file:
            # načteme seznam řádků do data
            data = file.readlines()    
        # nyní vybereme 2. a 4. řádek
        aktualniVerzeSVN = []
        radky = [1,3]
        for i in radky:
            # nacteni konkretniho radku
            heoCisloVerze = data[i]
            # posledni 4 cisla
            posledni4Cisla = int(heoCisloVerze[-5:])
            posledni4Cisla = str(posledni4Cisla).zfill(4)
            aktualniVerzeSVN.append(posledni4Cisla)

        return aktualniVerzeSVN


    def ziskaniCtyrCisli(self, soubor):
        self.soubor = soubor
        with open(self.soubor, 'r') as file:
            # načteme seznam řádků do data
            data = file.readlines()    
        # nyní změnime 2. a 4. řádek, všineme si, že musíme přidat nový řádek /n znamená že odskočíme na další řádku
        radky = [1,3]
        for i in radky:
            # nacteni konkretniho radku
            heoCisloVerze = data[i]    
            # verze bez posledniho 4 cisli
            zacatekCislaVerze = heoCisloVerze[:-5]
            # posledni 4 cisla
            posledni4CislaInt = int(heoCisloVerze[-5:])
            posledni4Cisla = str(posledni4CislaInt).zfill(4)
            return posledni4Cisla  

    def zvyseniVerze(self, soubor):
        self.soubor = soubor
        with open(self.soubor, 'r') as file:
            # načteme seznam řádků do data
            data = file.readlines()    
        # nyní změnime 2. a 4. řádek, všineme si, že musíme přidat nový řádek /n znamená že odskočíme na další řádku
        radky = [1,3]
        for i in radky:
            # nacteni konkretniho radku
            heoCisloVerze = data[i]    
            # verze bez posledniho 4 cisli
            zacatekCislaVerze = heoCisloVerze[:-5]
            # posledni 4 cisla
            posledni4Cisla = int(heoCisloVerze[-5:])
            zvyseny4Cisla = str(posledni4Cisla + 1).zfill(4)
            vyslednyStringVerze = zacatekCislaVerze + zvyseny4Cisla + '\n'
            data[i] = vyslednyStringVerze
        # and write everything back
        with open(self.soubor, 'w') as file:
            file.writelines(data)      

    def upraveniCommitSouboru(self, souborCommitSVN, zdroje, message, uvodCesty):
        self.souborCommitSVN = souborCommitSVN
        self.zdroje = zdroje
        self.message = message
        self.uvodCesty = uvodCesty

        with open(self.souborCommitSVN, 'r') as file:
            # načteme seznam řádků do data
            data = file.readlines()    
        # nyní změnime 14. řádek
        radek = 13    
        if self.zdroje == 'Ostre':        
            # nacteni konkretniho radku
            heoCisloVerze = data[radek]
            cestaNaSvn = '"c:\\Program Files\\TortoiseSVN\\bin\\svn.exe"'
            commit = 'commit' 
            konecCesty = '\\Ostre\\asseco\\_Verze.inc -m'
            celaCesta = self.uvodCesty + konecCesty
            msg = f'"{self.message}"'
            x = cestaNaSvn + ' ' + commit + ' ' + celaCesta + ' ' + msg + '\n'
            data[radek] = x
        elif self.zdroje == 'Stare':        
            # nacteni konkretniho radku
            heoCisloVerze = data[radek]
            cestaNaSvn = '"c:\\Program Files\\TortoiseSVN\\bin\\svn.exe"'
            commit = 'commit' 
            konecCesty = '\\Stare\\asseco\\_Verze.inc -m'
            celaCesta = self.uvodCesty + konecCesty
            msg = f'"{self.message}"'
            x = cestaNaSvn + ' ' + commit + ' ' + celaCesta + ' ' + msg + '\n'
            data[radek] = x
        else:        
            # nacteni konkretniho radku
            heoCisloVerze = data[radek]
            cestaNaSvn = '"c:\\Program Files\\TortoiseSVN\\bin\\svn.exe"'
            commit = 'commit' 
            konecCesty = '\\Freeze\\asseco\\_Verze.inc -m'
            celaCesta = self.uvodCesty + konecCesty
            msg = f'"{self.message}"'
            x = cestaNaSvn + ' ' + commit + ' ' + celaCesta + ' ' + msg + '\n'
            data[radek] = x

        with open(self.souborCommitSVN, 'w') as file:
            file.writelines(data) 

    def updateFromSVN(self, zdroje):
        self.zdroje = zdroje
        if self.zdroje == 'Ostre':
           subprocess.call([r'C:\Users\zdenek.ptak\Repository\CisloVerze\updateSvnOstre.bat'])
        elif self.zdroje == 'Stare':
           subprocess.call([r'C:\Users\zdenek.ptak\Repository\CisloVerze\updateSvnStare.bat'])
        else:
           subprocess.call([r'C:\Users\zdenek.ptak\Repository\CisloVerze\updateSvnFreeze.bat'])


    def commitToSVN(self): 
           subprocess.call([r'C:\Users\zdenek.ptak\Repository\CisloVerze\commitSvn.bat'])

    def ziskaniVerzeZIni(self, iniSoubor, zdroje):
        self.iniSoubor = iniSoubor
        self.zdroje = zdroje
        # instantiate
        config = ConfigParser()
        # načtení existujiciho souboru
        config.read(self.iniSoubor)
        # naštení hodnot z ini souboru
        if self.zdroje == 'Ostre':
            heo2verze = config.get('HeO2_Ostre', 'verze')
            heo3verze = config.get('HeO3_Ostre', 'verze')
        elif self.zdroje == 'Stare':
            heo2verze = config.get('HeO2_Stare', 'verze')
            heo3verze = config.get('HeO3_Stare', 'verze')
        else:
            heo2verze = config.get('HeO2_Freeze', 'verze')
            heo3verze = config.get('HeO3_Freeze', 'verze')
        return [heo2verze, heo3verze]

    def ulozeniDoIni(self, iniSoubor, zdroje, noveCisloVerze):
        self.iniSoubor = iniSoubor
        self.zdroje = zdroje
        self.noveCisloVerze = noveCisloVerze
        
        config = ConfigParser()
        config.read(self.iniSoubor)
        # zmena existujicich hodnot
        if self.zdroje == 'Ostre':
            config.set("HeO2_Ostre","verze", self.noveCisloVerze)
            config.set("HeO3_Ostre","verze", self.noveCisloVerze)
        elif self.zdroje == 'Stare':
            config.set("HeO2_Stare","verze", self.noveCisloVerze)
            config.set("HeO3_Stare","verze", self.noveCisloVerze)
        else:
            config.set("HeO2_Freeze","verze", self.noveCisloVerze)
            config.set("HeO3_Freeze","verze", self.noveCisloVerze)

        with open(self.iniSoubor, 'w') as configfile:
            config.write(configfile)

    def vyslednaZprava(self, cisloVerze):
        self.cisloVerze = cisloVerze
        msg = f"Automaticke zvyseni verze pro nocni buildy: {self.cisloVerze}"
        return msg  
    
    def dokonceni(self, zdroje, cesta, iniSoubor, vysledkyPoslednichZmen, souborCommitSVN, uvodCesty):
        self.zdroje = zdroje
        self.cesta = cesta
        self.iniSoubor = iniSoubor
        self.vysledkyPoslednichZmen = vysledkyPoslednichZmen
        self.souborCommitSVN = souborCommitSVN
        self.uvodCesty = uvodCesty
        
        verzovaciAutomat = VerzovaciAutomat()
        verzovaciAutomat.updateFromSVN(self.zdroje)
        aktualniSVN = verzovaciAutomat.aktualniVerzeSVN(self.cesta)
        aktualniINI = verzovaciAutomat.ziskaniVerzeZIni(self.iniSoubor, self.zdroje)
        print(f'Aktualni cislo verze na SVN - HeO2: {aktualniSVN[0]} a HeO3: {aktualniSVN[1]}')
        print(f'Aktualni cislo verze na SVN - HeO2: {aktualniINI[0]} a HeO3: {aktualniINI[1]}')

        if aktualniSVN[0] == aktualniINI[0] and aktualniSVN[1] == aktualniINI[1]:
            print(f"{self.zdroje}:  zdroje nebyly zvednuty manuálně")
            if self.vysledkyPoslednichZmen[self.zdroje] == True:
                print(f'{self.zdroje}:  do zdrojů byly vloženy úpravy')        
                verzovaciAutomat.zvyseniVerze(self.cesta)
                noveCisloVerze = verzovaciAutomat.ziskaniCtyrCisli(self.cesta)
                verzovaciAutomat.ulozeniDoIni(self.iniSoubor, self.zdroje, noveCisloVerze)
                message = verzovaciAutomat.vyslednaZprava(noveCisloVerze)
                print(message)
                verzovaciAutomat.upraveniCommitSouboru(self.souborCommitSVN, self.zdroje, message, self.uvodCesty)
                print(f"{self.zdroje}:  zdroje byly zvyseny na {noveCisloVerze}")
                print()
#                 verzovaciAutomat.commitToSVN()
            else:
                print(f"{self.zdroje}:  zdroje nebyly upraveny")  
                print()
        else:
            print(f"{self.zdroje}:  zdroje byly zvýšeny manuálně")
            verzovaciAutomat.ulozeniDoIni(self.iniSoubor, self.zdroje, aktualniSVN[0])
            print(f'{self.zdroje}:  do ini souboru do bylo vlozeno cislo verze - {aktualniSVN[0]}')
            print()