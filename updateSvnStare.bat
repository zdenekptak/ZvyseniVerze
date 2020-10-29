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
"c:\Program Files\TortoiseSVN\bin\svn.exe" update C:\HeO_vyroba_distribuce\Zdroje\Stare
  %osetrenichyby%
echo.
echo.
echo.
echo.


exit
