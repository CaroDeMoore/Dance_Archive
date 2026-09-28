@echo off
rem -----------------------------------------------
rem Build main.py als EXE 
rem -----------------------------------------------

rem Voraussetzungen
rem     Komponenten müssen im .venv-Ordner installiert werden:
rem         pip install pyinstaller
rem         ... hier fehlt noch was
rem     .venv aktivieren:
rem         Scripts\activate

rem Zielarchiv:
set DIST=..\ArchivA
rem Quelle ist main.py
set SRC=main.py
rem Arbeitsordner für PyInstaller, wird nach dem Build gelöscht
set WORK=build

if exist %WORK% rmdir /s /q %WORK%
rem !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
rem Niemals den Zielordner löschen und neu erstellen.
rem !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

pyinstaller --clean --onedir --console ^
    --distpath "%DIST%" ^
    --workpath "%WORK%" ^
    "%SRC%" ^
    --name "TanzArchiv" 
    rem > _build.log 2>&1
    rem --icon "src\icon.ico"

IF ERRORLEVEL 1 (
    echo Fehler beim Build
    exit /b %ERRORLEVEL%
)

if exist %WORK% rmdir /s /q %WORK%
if exist main.spec del main.spec

echo.
echo Build abgeschlossen.
pause