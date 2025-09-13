@REM @echo off
@REM REM build_portable.bat
@REM REM Baut file_sorter.exe aus main.py mit PyInstaller

@REM REM Prüfen ob Python installiert ist
@REM python --version >nul 2>&1
@REM if ERRORLEVEL 1 (
@REM     echo ERROR: Python wurde nicht gefunden. Bitte zuerst Python installieren.
@REM     pause
@REM     exit /b 1
@REM )

@REM REM Prüfen ob PyInstaller installiert ist
@REM python -m pyinstaller --version >nul 2>&1
@REM if ERRORLEVEL 1 (
@REM     echo PyInstaller ist nicht installiert. Installiere...
@REM     python -m pip install --upgrade pip
@REM     python -m pip install pyinstaller tkinterdnd2
@REM )

@REM REM Pfad zu tkdnd2.8 anpassen
@REM set "TKDND_PATH=C:\Users\benja\AppData\Local\Programs\Python\Python312\tcl\tkdnd2.8"

@REM REM Baue portable EXE mit tkdnd2.8
@REM python -m PyInstaller ^
@REM   --noconfirm --clean --onefile --windowed ^
@REM   --name file_sorter ^
@REM   --hidden-import tkinterdnd2 ^
@REM   --add-data "%TKDND_PATH%;tkdnd2.8" ^
@REM   "main.py"

@REM REM Ergebnis prüfen
@REM if exist "dist\file_sorter.exe" (
@REM     echo Build erfolgreich: dist\file_sorter.exe
@REM ) else (
@REM     echo FEHLER: dist\file_sorter.exe nicht gefunden!
@REM )

@REM REM Aufräumen (nur Build-Reste, dist bleibt erhalten)
@REM rmdir /s /q build >nul 2>&1
@REM del /q "file_sorter.spec" >nul 2>&1

@REM echo Fertig.
@REM pause


@echo off
REM build_portable.bat
REM Baut file_sorter.exe aus main.py mit PyInstaller

REM Prüfen ob Python installiert ist
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python wurde nicht gefunden. Bitte zuerst Python installieren.
    pause
    exit /b 1
)

REM Prüfen ob PyInstaller installiert ist
python -m pyinstaller --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller ist nicht installiert. Installiere...
    python -m pip install --upgrade pip
    python -m pip install pyinstaller tkinterdnd2
)

REM >>> Hier TkDND-Pfad dynamisch ermitteln
for /f "delims=" %%i in ('python -c "import os,tkinterdnd2; print(os.path.join(os.path.dirname(tkinterdnd2.__file__), 'tkdnd'))"') do set "TKDND_PATH=%%i"

echo Gefundener tkdnd-Pfad: %TKDND_PATH%

REM Baue portable EXE mit automatisch gefundenem tkdnd
python -m PyInstaller ^
  --noconfirm --clean --onefile --windowed ^
  --name file_sorter ^
  --hidden-import tkinterdnd2 ^
  --add-data "%TKDND_PATH%;tkinterdnd2/tkdnd" ^
  "main.py"

REM Ergebnis prüfen
if exist "dist\file_sorter.exe" (
    echo Build erfolgreich: dist\file_sorter.exe
) else (
    echo FEHLER: dist\file_sorter.exe nicht gefunden!
)

REM Aufräumen (nur Build-Reste, dist bleibt erhalten)
rmdir /s /q build >nul 2>&1
del /q "file_sorter.spec" >nul 2>&1

echo Fertig.
pause
