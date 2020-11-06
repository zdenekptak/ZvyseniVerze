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
"c:\Program Files\TortoiseSVN\bin\svn.exe" commit C:\HeO_vyroba_distribuce\Zdroje\Stare\asseco\_Verze.inc -m "Automatické zvýšení verze pro noèní buildy: 0949"
echo.
echo.
echo.
echo.

echo.
echo automaticke pozdrzeni davky na 5 sec 
choice /C A /D A /T 5 > nul


exit
