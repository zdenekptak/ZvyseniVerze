@echo off
title Aktualizace zdrojaku HELIOS ORANGE

echo SVN UPDATE (aktualizace ze SVN na lokal)

set osetrenichyby=IF %ERRORLEVEL% EQU 1 msg %username% Chyba pri aktualizaci zdroju!

echo.
echo.
echo.
echo ===== ostre zdroje ========================================
"c:\Program Files\TortoiseSVN\bin\svn.exe" info https://svn-cz.asol.local/svn/HeliosOrange/heo/trunk/asseco
echo.
"c:\Program Files\TortoiseSVN\bin\svn.exe" commit C:\HeO_vyroba_distribuce\Zdroje\Ostre\asseco\_Verze - kopie.inc -m "Automatick� zv��en� verze pro no�n� buildy: 0986"
echo.
echo.
echo.
echo.

echo.
echo automaticke pozdrzeni davky na 30 sec 
choice /C A /D A /T 30 > nul


exit