@echo off
title Aktualizace zdrojaku HELIOS ORANGE

echo COMMIT do SVN

set osetrenichyby=IF %ERRORLEVEL% EQU 1 msg %username% Chyba pri aktualizaci zdroju!

echo.
echo.
echo.
echo ===== ostre zdroje ========================================
"c:\Program Files\TortoiseSVN\bin\svn.exe" info https://svn-cz.asol.local/svn/HeliosOrange/heo/trunk/asseco
echo.
"c:\Program Files\TortoiseSVN\bin\svn.exe" commit C:\HeO_vyroba_distribuce\Zdroje\Stare\asseco\_Verze.inc -m "Automaticke zvyseni verze pro nocni buildy: 0116"
echo.
echo.
echo.
echo.
SET cil=C:\Users\zdenek.ptak\Repository\CisloVerze

ECHO %DATE% %TIME% kontrola spusteni bataku Commit SVN >> %cil%\_aktualizace_.txt
echo.
echo automaticke pozdrzeni davky na 5 sec 
choice /C A /D A /T 5 > nul


exit
