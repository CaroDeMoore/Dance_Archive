@echo off
REM ===============================
REM Robocopy für Offline-Website auf Android
REM ===============================

REM Quellordner auf dem PC
set SOURCE_video=C:\Users\Volker\Documents\Tanzen\HTML_Writer\videothek
set SOURCE_html=C:\Users\Volker\Documents\Tanzen\HTML_Writer\html

REM Zielordner auf Android (über USB / MTP gemountet)
set DEST_video=E:\MeineWebseite
set DEST_html=E:\MeineWebseite

REM Robocopy Optionen:
REM /MIR -> Spiegelung der Ordnerstruktur
REM /XO  -> Überspringt ältere Dateien
REM /FFT -> Toleranz bei Zeitstempeln (2 Sekunden, nützlich bei MTP)
REM /R:2 -> Anzahl Wiederholungen bei Fehlern
REM /W:2 -> Wartezeit zwischen Wiederholungen
REM /LOG -> Optional: Log-Datei erstellen

robocopy "%SOURCE_video%" "%DEST_video%" /MIR /XO /FFT /R:2 /W:2 /LOG:"C:\MeineWebseite\sync_log.txt"
robocopy "%SOURCE_html%" "%DEST_html%" /MIR /XO /FFT /R:2 /W:2 /LOG:"C:\MeineWebseite\sync_log.txt"

echo.
echo ===============================
echo Synchronisation abgeschlossen.
echo Nur neue oder geänderte Dateien wurden kopiert.
pause