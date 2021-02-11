@echo off
title Aktualizace zdrojaku HELIOS ORANGE

echo.
echo.
echo.
echo.
echo SVN UPDATE (aktualizace ze SVN na lokal)
echo ===== freeze zdroje ========================================
"c:\Program Files\TortoiseSVN\bin\svn.exe" info https://svn-cz.asol.local/svn/HeliosOrange/heo/trunk/asseco
echo.
"c:\Program Files\TortoiseSVN\bin\svn.exe" update C:\HeO_vyroba_distribuce\Zdroje\Freeze
echo.

SET cil=C:\Users\zdenek.ptak\Repository\CisloVerze

ECHO %DATE% %TIME% kontrola spusteni bataku update freeze >> %cil%\_aktualizace_.txt


echo automaticke pozdrzeni davky na 5 sec 
choice /C A /D A /T 5 > nul

exit
