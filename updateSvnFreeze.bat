@echo off
title Aktualizace zdrojaku HELIOS ORANGE

echo SVN UPDATE (aktualizace ze SVN na lokal)

set osetrenichyby=IF %ERRORLEVEL% EQU 1 msg %username% Chyba pri aktualizaci zdroju!

echo.
echo ===== freeze zdroje ========================================
"c:\Program Files\TortoiseSVN\bin\svn.exe" info https://svn-cz.asol.local/svn/HeliosOrange/heo/trunk/asseco
echo.
"c:\Program Files\TortoiseSVN\bin\svn.exe" update C:\HeO_vyroba_distribuce\Zdroje\Freeze
  %osetrenichyby%
echo.
echo automaticke pozdrzeni davky na 2 sec 
choice /C A /D A /T 2 > nul

exit
