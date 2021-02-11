@echo off
title Zvyseni verze  
echo.

SET cil=C:\Users\zdenek.ptak\Repository\CisloVerze

cd C:\Users\zdenek.ptak\Repository\CisloVerze\

run.py > %cil%\_testVerzeUp_.txt


echo automaticke pozdrzeni davky na 10 sec 
choice /C A /D A /T 10 > nul
