@echo off
%~d0
cd %~dp0

set xpPath=%localappdata%
set sevenPath=%userprofile%\Local Settings\Application Data

:: Document Basket
rmdir /s /q "%sevenPath%\DocumentBasket" > nul 2>&1
rmdir /s /q "%xpPath%\DocumentBasket" > nul 2>&1

:: Document Modeler
rmdir /s /q "%sevenPath%\DocumentModeler" > nul 2>&1
rmdir /s /q "%xpPath%\DocumentModeler" > nul 2>&1

:: Document Scanner
rmdir /s /q "%sevenPath%\DocumentScanner" > nul 2>&1
rmdir /s /q "%xpPath%\DocumentScanner" > nul 2>&1

:: Touch Scanner
rmdir /s /q "%sevenPath%\TouchScanner" > nul 2>&1
rmdir /s /q "%xpPath%\TouchScanner" > nul 2>&1

:: PDF Editor
rmdir /s /q "%sevenPath%\PDFEditor\Temp" > nul 2>&1
rmdir /s /q "%xpPath%\PDFEditor\Temp" > nul 2>&1

:: Wizard
del /f /s /q "%sevenPath%\Wizard\Backup\*.*" > nul 2>&1
del /f /s /q "%sevenPath%\Wizard\Temp\*.*" > nul 2>&1
del /f /s /q "%xpPath%\Wizard\Backup\*.*" > nul 2>&1
del /f /s /q "%xpPath%\Wizard\Temp\*.*" > nul 2>&1

:End